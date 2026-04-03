from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Worker, Admin
from app.ml_engine import compute_risk_score, recommend_plan, calculate_dynamic_premium
import uuid, random
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    name:     str
    phone:    str
    email:    str
    password: str
    platform: str
    zone:     str
    pincode:  str
    aadhaar:  str
    bank_upi_id: str = None
    plan:     str = None

class LoginRequest(BaseModel):
    email:    str
    password: str
    role:     str = "worker"

class OTPRequest(BaseModel):
    phone: str
    aadhaar: str

class OTPVerify(BaseModel):
    phone: str
    otp:   str

# In-memory OTP store (mock)
OTP_STORE = {}

@router.post("/otp/send")
def send_otp(req: OTPRequest):
    otp = str(random.randint(100000, 999999))
    OTP_STORE[req.phone] = otp
    print(f"[MOCK OTP] Phone: {req.phone} → OTP: {otp}")
    return {
        "success": True,
        "message": f"OTP sent to {req.phone[:6]}XXXX",
        "mock_otp": otp,  # shown in demo mode
    }

@router.post("/otp/verify")
def verify_otp(req: OTPVerify):
    stored = OTP_STORE.get(req.phone)
    if not stored:
        raise HTTPException(400, "OTP not sent or expired")
    if stored != req.otp:
        raise HTTPException(400, "Invalid OTP")
    OTP_STORE.pop(req.phone, None)
    return {"success": True, "verified": True}

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # Check duplicate
    if db.query(Worker).filter(Worker.email == req.email).first():
        raise HTTPException(400, "Email already registered")
    if db.query(Worker).filter(Worker.phone == req.phone).first():
        raise HTTPException(400, "Phone already registered")

    month      = datetime.now().month
    risk_score = compute_risk_score(req.zone, month)
    rec_plan   = recommend_plan(risk_score)
    final_plan = req.plan if req.plan else rec_plan
    premium    = calculate_dynamic_premium(req.zone, final_plan, month)

    worker = Worker(
        id               = "WKR-" + uuid.uuid4().hex[:4].upper(),
        name             = req.name,
        phone            = req.phone,
        email            = req.email,
        password         = req.password,
        platform         = req.platform,
        zone             = req.zone,
        pincode          = req.pincode,
        aadhaar_verified = True,
        plan             = final_plan,
        risk_score       = risk_score,
        trust_score      = 40,
        bank_upi_id      = req.bank_upi_id,
    )
    db.add(worker)
    db.commit()
    db.refresh(worker)

    return {
        "success":          True,
        "worker_id":        worker.id,
        "name":             worker.name,
        "zone":             worker.zone,
        "plan":             final_plan,
        "risk_score":       risk_score,
        "recommended_plan": rec_plan,
        "premium":          premium,
        "trust_score":      40,
        "role":             "worker",
        "message":          f"Welcome to GigSecure, {worker.name}!",
    }

@router.post("/login")
def login(req: LoginRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from app.tasks import verify_worker_integrity
    if req.role == "admin":
        user = db.query(Admin).filter(Admin.email == req.email).first()
        if not user or user.password != req.password:
            raise HTTPException(401, "Invalid credentials")
        return {
            "success": True, "role": "admin",
            "id": user.id, "name": user.name,
            "email": user.email, "org": user.org,
        }
    else:
        user = db.query(Worker).filter(Worker.email == req.email).first()
        if not user or user.password != req.password:
            raise HTTPException(401, "Invalid credentials")
        
        # Trigger background integrity scan
        background_tasks.add_task(verify_worker_integrity, user.id)
        
        return {
            "success":     True, "role": "worker",
            "id":          user.id, "name": user.name,
            "email":       user.email, "phone": user.phone,
            "zone":        user.zone, "plan": user.plan,
            "risk_score":  user.risk_score, "trust_score": user.trust_score,
            "payouts":     user.payouts, "sim_payouts": user.sim_payouts,
            "claims_total":user.claims_total, "platform": user.platform,
            "pincode":     user.pincode, "weekly_hrs_used": user.weekly_hrs_used,
            "bank_upi_id": user.bank_upi_id,
        }

@router.get("/worker/{worker_id}")
def get_worker(worker_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from app.tasks import verify_worker_integrity
    # Check integrity every time profile is fetched
    background_tasks.add_task(verify_worker_integrity, worker_id)
    
    w = db.query(Worker).filter(Worker.id == worker_id).first()
    if not w:
        raise HTTPException(404, "Worker not found")
    return {
        "id": w.id, "name": w.name, "phone": w.phone,
        "email": w.email, "zone": w.zone, "plan": w.plan,
        "risk_score": w.risk_score, "trust_score": w.trust_score,
        "payouts": w.payouts, "sim_payouts": w.sim_payouts,
        "claims_total": w.claims_total, "platform": w.platform,
        "joined": str(w.joined), "weekly_hrs_used": w.weekly_hrs_used,
        "aadhaar_verified": w.aadhaar_verified, "bank_upi_id": w.bank_upi_id,
    }

@router.get("/workers")
def get_all_workers(db: Session = Depends(get_db)):
    workers = db.query(Worker).all()
    return [
        {
            "id": w.id, "name": w.name, "phone": w.phone,
            "email": w.email, "zone": w.zone, "plan": w.plan,
            "risk_score": w.risk_score, "trust_score": w.trust_score,
            "payouts": w.payouts, "sim_payouts": w.sim_payouts,
            "claims_total": w.claims_total, "platform": w.platform,
            "joined": str(w.joined), "is_active": w.is_active,
            "weekly_hrs_used": w.weekly_hrs_used,
        }
        for w in workers
    ]

@router.put("/worker/{worker_id}")
def update_worker(worker_id: str, patch: dict, db: Session = Depends(get_db)):
    w = db.query(Worker).filter(Worker.id == worker_id).first()
    if not w:
        raise HTTPException(404, "Worker not found")
    for key, value in patch.items():
        if hasattr(w, key):
            setattr(w, key, value)
    db.commit()
    db.refresh(w)
    return {"success": True, "worker_id": worker_id}

@router.post("/admin/register")
def register_admin(data: dict, db: Session = Depends(get_db)):
    admin = Admin(
        id = "ADM-" + uuid.uuid4().hex[:4].upper(),
        name = data.get("name"),
        email = data.get("email"),
        password = data.get("password", "admin123"),
        org = data.get("org", "GigSecure"),
        designation = data.get("designation", "Admin"),
    )
    db.add(admin)
    db.commit()
    return {"success": True, "admin_id": admin.id}

@router.get("/admins")
def get_all_admins(db: Session = Depends(get_db)):
    admins = db.query(Admin).all()
    return {
        "admins": [
            {
                "id": a.id, "name": a.name, "email": a.email,
                "org": a.org, "designation": a.designation,
                "phone": a.phone, "joined": str(a.joined),
                "role": "admin"
            }
            for a in admins
        ]
    }