from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from app.database import get_db
from app.models import Worker, Admin
from app.ml_engine import compute_risk_score, recommend_plan, calculate_dynamic_premium
from app.security import hash_password, verify_password, create_access_token, verify_token
import uuid, random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

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
    
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v
    
    @validator("phone")
    def validate_phone(cls, v):
        if not v.startswith("+91") and len(v.replace(" ", "")) < 10:
            raise ValueError("Invalid phone number")
        return v

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

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    worker_id: str
    role: str

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
    """Register new worker with secure password hashing."""
    # Check duplicate
    if db.query(Worker).filter(Worker.email == req.email).first():
        raise HTTPException(400, "Email already registered")
    if db.query(Worker).filter(Worker.phone == req.phone).first():
        raise HTTPException(400, "Phone already registered")

    try:
        month      = datetime.now().month
        risk_score = compute_risk_score(req.zone, month)
        rec_plan   = recommend_plan(risk_score)
        final_plan = req.plan if req.plan else rec_plan
        premium    = calculate_dynamic_premium(req.zone, final_plan, month)

        # Hash password securely
        hashed_pwd = hash_password(req.password)

        worker = Worker(
            id               = "WKR-" + uuid.uuid4().hex[:4].upper(),
            name             = req.name,
            phone            = req.phone,
            email            = req.email,
            password         = hashed_pwd,  # Store hashed password
            platform         = req.platform,
            zone             = req.zone,
            pincode          = req.pincode,
            aadhaar_verified = True,
            plan             = final_plan,
            risk_score       = risk_score,
            trust_score      = 40,
            bank_upi_id      = req.bank_upi_id,
            plan_effective_date = datetime.now(),
        )
        db.add(worker)
        db.commit()
        db.refresh(worker)
        
        # Generate JWT token
        token = create_access_token({"worker_id": worker.id, "role": "worker"})

        logger.info(f"✅ Worker registered: {worker.id} | {worker.name}")

        return {
            "success":          True,
            "access_token":     token,
            "token_type":       "bearer",
            "worker_id":        worker.id,
            "name":             worker.name,
            "zone":             worker.zone,
            "plan":             final_plan,
            "risk_score":       risk_score,
            "recommended_plan": rec_plan,
            "premium":          premium,
            "trust_score":      40,
            "role":             "worker",
            "message":          f"✅ Welcome to GigSecure, {worker.name}!",
        }
    except ValueError as e:
        logger.error(f"❌ Registration validation error: {e}")
        raise HTTPException(400, str(e))
    except Exception as e:
        logger.error(f"❌ Registration error: {e}")
        db.rollback()
        raise HTTPException(500, "Registration failed")

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Login with JWT token generation."""
    try:
        if req.role == "admin":
            user = db.query(Admin).filter(Admin.email == req.email).first()
            if not user:
                logger.warning(f"⚠️  Admin login attempt - user not found: {req.email}")
                raise HTTPException(401, "Invalid credentials")
            
            # Verify password hash
            if not verify_password(req.password, user.password):
                logger.warning(f"⚠️  Admin login attempt - invalid password: {req.email}")
                raise HTTPException(401, "Invalid credentials")
            
            # Generate JWT token
            token = create_access_token({"admin_id": user.id, "role": "admin"})
            
            logger.info(f"✅ Admin logged in: {user.id} | {user.name}")
            
            return TokenResponse(access_token=token, token_type="bearer", worker_id=user.id, role="admin")
        
        else:
            user = db.query(Worker).filter(Worker.email == req.email).first()
            if not user:
                logger.warning(f"⚠️  Worker login attempt - user not found: {req.email}")
                raise HTTPException(401, "Invalid credentials")
            
            # Verify password hash
            if not verify_password(req.password, user.password):
                logger.warning(f"⚠️  Worker login attempt - invalid password: {req.email}")
                raise HTTPException(401, "Invalid credentials")
            
            # Generate JWT token
            token = create_access_token({"worker_id": user.id, "role": "worker"})
            
            logger.info(f"✅ Worker logged in: {user.id} | {user.name}")
            
            # Trigger background integrity scan
            from app.tasks import verify_worker_integrity
            background_tasks.add_task(verify_worker_integrity, user.id)
            
            return TokenResponse(access_token=token, token_type="bearer", worker_id=user.id, role="worker")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        raise HTTPException(500, "Login failed")

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
        "earnings_protected": w.earnings_protected,
        "claims_total": w.claims_total, 
        "claims_approved": w.claims_approved,
        "claims_rejected": w.claims_rejected,
        "platform": w.platform,
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