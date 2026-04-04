"""
KYC Routes — Simulated Aadhaar verification (UIDAI mock)
Endpoints: /kyc/initiate · /kyc/verify-otp · /kyc/status/{worker_id}
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Worker, KYCRecord, NotificationLog
import random, uuid
from datetime import datetime

router = APIRouter(prefix="/kyc", tags=["kyc"])

# In-memory OTP store (for hackathon demo)
OTP_STORE = {}

class KYCInitiate(BaseModel):
    worker_id:      str
    aadhaar_number: str
    phone:          str

class KYCVerify(BaseModel):
    worker_id: str
    phone:     str
    otp:       str

class OTPSend(BaseModel):
    phone:   str
    aadhaar: str

class OTPVerifyReq(BaseModel):
    phone: str
    otp:   str

def _validate_aadhaar(num: str) -> bool:
    """Basic Aadhaar validation: 12 digits, not all same."""
    clean = num.replace(" ", "").replace("-", "")
    return clean.isdigit() and len(clean) == 12 and len(set(clean)) > 1

# ─────────────────────────────────────────────────────────────────────────────
# OTP Send (standalone — used in onboarding before registration)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/otp/send")
def send_otp(req: OTPSend):
    if not _validate_aadhaar(req.aadhaar):
        raise HTTPException(400, "Invalid Aadhaar number — must be 12 digits")
    otp = str(random.randint(100000, 999999))
    OTP_STORE[req.phone] = {"otp": otp, "aadhaar": req.aadhaar, "created_at": datetime.now()}
    return {
        "success":  True,
        "message":  f"OTP sent to {req.phone[:6]}XXXX via UIDAI mock",
        "mock_otp": otp,   # shown in demo mode
        "expires_in": 300, # 5 minutes
    }

@router.post("/otp/verify")
def verify_otp(req: OTPVerifyReq):
    stored = OTP_STORE.get(req.phone)
    if not stored:
        raise HTTPException(400, "OTP not sent or expired — request a new OTP")
    if stored["otp"] != req.otp:
        raise HTTPException(400, "Invalid OTP — please try again")
    OTP_STORE.pop(req.phone, None)
    return {"success": True, "verified": True, "message": "Phone verified successfully"}

# ─────────────────────────────────────────────────────────────────────────────
# KYC Initiate (after registration — starts Aadhaar check)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/initiate")
def initiate_kyc(req: KYCInitiate, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == req.worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")

    if not _validate_aadhaar(req.aadhaar_number):
        raise HTTPException(400, "Invalid Aadhaar — must be 12 digits")

    if worker.aadhaar_verified:
        return {"success": True, "status": "already_verified", "message": "Aadhaar already verified"}

    otp = str(random.randint(100000, 999999))
    OTP_STORE[req.phone] = {"otp": otp, "aadhaar": req.aadhaar_number, "worker_id": req.worker_id}

    # Store KYC record
    kyc = KYCRecord(
        id             = "KYC-" + uuid.uuid4().hex[:6].upper(),
        worker_id      = req.worker_id,
        aadhaar_number = req.aadhaar_number[-4:].zfill(12),  # masked
        phone          = req.phone,
        otp            = otp,
        status         = "otp_sent",
    )
    db.add(kyc)
    db.commit()

    return {
        "success":    True,
        "status":     "otp_sent",
        "kyc_id":     kyc.id,
        "message":    f"OTP sent to {req.phone[:6]}XXXX — valid 5 minutes",
        "mock_otp":   otp,
    }

# ─────────────────────────────────────────────────────────────────────────────
# KYC Verify OTP
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/verify")
def verify_kyc(req: KYCVerify, db: Session = Depends(get_db)):
    stored = OTP_STORE.get(req.phone)
    if not stored:
        raise HTTPException(400, "OTP expired or not sent — initiate KYC again")
    if stored["otp"] != req.otp:
        # Track failed attempts
        kyc = db.query(KYCRecord).filter(
            KYCRecord.worker_id == req.worker_id,
            KYCRecord.status    == "otp_sent"
        ).first()
        if kyc:
            kyc.attempts = (kyc.attempts or 0) + 1
            db.commit()
        raise HTTPException(400, "Invalid OTP")

    OTP_STORE.pop(req.phone, None)
    worker = db.query(Worker).filter(Worker.id == req.worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")

    worker.aadhaar_verified = True
    worker.aadhaar_number   = stored.get("aadhaar", "")

    kyc = db.query(KYCRecord).filter(
        KYCRecord.worker_id == req.worker_id,
        KYCRecord.status    == "otp_sent"
    ).first()
    if kyc:
        kyc.status      = "verified"
        kyc.verified_at = datetime.now()

    # KYC success notification
    notif = NotificationLog(
        worker_id  = req.worker_id,
        title      = "✅ Aadhaar KYC Verified",
        message    = "Your identity has been verified. Full coverage benefits are now active.",
        notif_type = "kyc_done",
        icon       = "✅",
    )
    db.add(notif)
    db.commit()

    return {
        "success":   True,
        "status":    "verified",
        "worker_id": req.worker_id,
        "message":   "Aadhaar KYC verified successfully. Full benefits unlocked.",
    }

# ─────────────────────────────────────────────────────────────────────────────
# KYC Status
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/status/{worker_id}")
def kyc_status(worker_id: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")
    kyc = db.query(KYCRecord).filter(
        KYCRecord.worker_id == worker_id
    ).order_by(KYCRecord.created_at.desc()).first()
    return {
        "worker_id":        worker_id,
        "aadhaar_verified": worker.aadhaar_verified,
        "status":           kyc.status if kyc else "not_initiated",
        "verified_at":      str(kyc.verified_at) if kyc and kyc.verified_at else None,
        "trust_boost":      "+10 trust score on verification" if not worker.aadhaar_verified else None,
    }
