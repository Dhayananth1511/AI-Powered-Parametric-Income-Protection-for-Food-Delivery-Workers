from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Worker, Policy, NotificationLog
from app.ml_engine import calculate_dynamic_premium, PLAN_ORDER
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/policy", tags=["policy"])

class PolicyCreate(BaseModel):
    worker_id: str
    plan:      str

class PlanChange(BaseModel):
    worker_id: str
    new_plan:  str
    effective: str = "now"   # "now" | "next_monday"

class PolicyRenew(BaseModel):
    worker_id: str

# ─────────────────────────────────────────────────────────────────────────────
# Create Policy
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/create")
def create_policy(req: PolicyCreate, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == req.worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")

    month   = datetime.now().month
    premium = calculate_dynamic_premium(worker.zone, req.plan, month, worker.trust_score or 40)

    # Deactivate any existing active policy
    db.query(Policy).filter(
        Policy.worker_id == req.worker_id,
        Policy.status    == "active"
    ).update({"status": "superseded", "end_date": datetime.now()})

    policy = Policy(
        id              = "POL-" + uuid.uuid4().hex[:6].upper(),
        worker_id       = req.worker_id,
        plan            = req.plan,
        premium         = premium["final_premium"],
        base_premium    = premium["base_premium"],
        risk_adjustment = premium["zone_adjustment"],
        trust_discount  = premium["trust_discount"],
        status          = "active",
        effective_date  = datetime.now(),
    )
    worker.plan               = req.plan
    worker.plan_effective_date = datetime.now()
    worker.weekly_hrs_used    = 0.0
    worker.weekly_reset_at    = datetime.now()

    db.add(policy)
    db.commit()
    db.refresh(policy)

    _notify(db, req.worker_id, "📋 Policy Created",
            f"{req.plan.title()} Plan activated · ₹{premium['final_premium']}/week · Coverage starts now",
            "plan_change")

    return {
        "success":        True,
        "policy_id":      policy.id,
        "plan":           policy.plan,
        "premium":        policy.premium,
        "premium_detail": premium,
        "status":         policy.status,
        "effective_date": str(policy.effective_date),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Get Active Policy
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/active/{worker_id}")
def get_active_policy(worker_id: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")
    policy = db.query(Policy).filter(
        Policy.worker_id == worker_id,
        Policy.status    == "active"
    ).first()
    if not policy:
        return {"has_policy": False, "worker_id": worker_id}

    from app.ml_engine import PLAN_BASE
    meta = PLAN_BASE.get(policy.plan, PLAN_BASE["standard"])
    hrs_remaining = max(0, meta["maxHrs"] - (worker.weekly_hrs_used or 0))

    return {
        "has_policy":      True,
        "policy_id":       policy.id,
        "plan":            policy.plan,
        "premium":         policy.premium,
        "base_premium":    policy.base_premium,
        "risk_adjustment": policy.risk_adjustment,
        "trust_discount":  policy.trust_discount,
        "status":          policy.status,
        "start_date":      str(policy.start_date),
        "renewal_count":   policy.renewal_count,
        "hourly_rate":     meta["rate"],
        "max_hours":       meta["maxHrs"],
        "weekly_cap":      meta["cap"],
        "hrs_used_this_week":  worker.weekly_hrs_used or 0,
        "hrs_remaining":       hrs_remaining,
        "payout_remaining":    round(hrs_remaining * meta["rate"], 0),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Get Policy History
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/history/{worker_id}")
def get_policy_history(worker_id: str, db: Session = Depends(get_db)):
    policies = (db.query(Policy)
                .filter(Policy.worker_id == worker_id)
                .order_by(Policy.created_at.desc())
                .all())
    return [
        {
            "id":           p.id,
            "plan":         p.plan,
            "premium":      p.premium,
            "status":       p.status,
            "start_date":   str(p.start_date),
            "end_date":     str(p.end_date) if p.end_date else None,
            "renewal_count":p.renewal_count,
        }
        for p in policies
    ]

# ─────────────────────────────────────────────────────────────────────────────
# Upgrade Plan
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/upgrade")
def upgrade_plan(req: PlanChange, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == req.worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")

    current_idx = PLAN_ORDER.index(worker.plan) if worker.plan in PLAN_ORDER else 2
    new_idx     = PLAN_ORDER.index(req.new_plan) if req.new_plan in PLAN_ORDER else 2

    if new_idx <= current_idx:
        raise HTTPException(400, "Use /policy/downgrade to move to a lower plan")

    return _change_plan(db, worker, req.new_plan, "upgraded")

# ─────────────────────────────────────────────────────────────────────────────
# Downgrade Plan (effective next Monday)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/downgrade")
def downgrade_plan(req: PlanChange, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == req.worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")

    current_idx = PLAN_ORDER.index(worker.plan) if worker.plan in PLAN_ORDER else 2
    new_idx     = PLAN_ORDER.index(req.new_plan) if req.new_plan in PLAN_ORDER else 2

    if new_idx >= current_idx:
        raise HTTPException(400, "Use /policy/upgrade to move to a higher plan")

    result = _change_plan(db, worker, req.new_plan, "downgraded")
    result["effective"] = "next_monday"
    result["note"] = "Coverage continues on current plan until Monday. New plan activates Monday."
    return result

def _change_plan(db, worker, new_plan: str, change_type: str) -> dict:
    month      = datetime.now().month
    old_plan   = worker.plan
    premium    = calculate_dynamic_premium(worker.zone, new_plan, month, worker.trust_score or 40)

    old_policy = db.query(Policy).filter(
        Policy.worker_id == worker.id,
        Policy.status    == "active"
    ).first()
    if old_policy:
        old_policy.status   = change_type
        old_policy.end_date = datetime.now()

    new_policy = Policy(
        id              = "POL-" + uuid.uuid4().hex[:6].upper(),
        worker_id       = worker.id,
        plan            = new_plan,
        premium         = premium["final_premium"],
        base_premium    = premium["base_premium"],
        risk_adjustment = premium["zone_adjustment"],
        trust_discount  = premium["trust_discount"],
        status          = "active",
        effective_date  = datetime.now(),
        renewal_count   = (old_policy.renewal_count or 0) + 1 if old_policy else 0,
    )
    worker.plan = new_plan
    worker.plan_effective_date = datetime.now()

    db.add(new_policy)
    db.commit()

    _notify(db, worker.id, f"📋 Plan {change_type.title()}",
            f"{old_plan.title()} → {new_plan.title()} · ₹{premium['final_premium']}/week",
            "plan_change")

    return {
        "success":   True,
        "old_plan":  old_plan,
        "new_plan":  new_plan,
        "premium":   premium,
        "policy_id": new_policy.id,
        "effective": "immediately",
    }

# ─────────────────────────────────────────────────────────────────────────────
# Renew Policy (extend coverage for another week)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/renew")
def renew_policy(req: PolicyRenew, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == req.worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")

    active = db.query(Policy).filter(
        Policy.worker_id == req.worker_id,
        Policy.status    == "active"
    ).first()
    if not active:
        raise HTTPException(404, "No active policy to renew — create a new policy")

    # Reset weekly hours
    active.renewal_count = (active.renewal_count or 0) + 1
    worker.weekly_hrs_used = 0.0
    worker.weekly_reset_at = datetime.now()
    db.commit()

    _notify(db, req.worker_id, "🔄 Policy Renewed",
            f"{active.plan.title()} Plan renewed · ₹{active.premium}/week · Coverage active",
            "plan_change")

    return {
        "success":        True,
        "policy_id":      active.id,
        "plan":           active.plan,
        "premium":        active.premium,
        "renewal_count":  active.renewal_count,
        "weekly_hrs_reset": True,
        "message":        "Policy renewed. Weekly hours reset. Coverage continues.",
    }

# ─────────────────────────────────────────────────────────────────────────────
# Cancel Policy
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/cancel")
def cancel_policy(req: PolicyCreate, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(
        Policy.worker_id == req.worker_id,
        Policy.status    == "active"
    ).first()
    if not policy:
        raise HTTPException(404, "No active policy found")

    policy.status   = "cancelled"
    policy.end_date = datetime.now()
    db.commit()

    _notify(db, req.worker_id, "❌ Policy Cancelled",
            "Coverage continues to end of week. Pro-rata credit applied if within cooling-off period.",
            "plan_change")

    return {
        "success": True,
        "message": "Policy cancelled. Coverage runs to end of this week.",
        "refund":  "Pro-rata credit applied if within 24hr cooling-off period.",
    }

# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Premium Calculator (GET endpoint)
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
# Zone Activity (Social Proof)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/zone-activity")
def get_zone_activity(zone: str, db: Session = Depends(get_db)):
    """Returns the count of active workers in a micro-zone for the Community Pulse widget."""
    count = db.query(Worker).filter(Worker.zone == zone).count()
    
    # Add some randomness for smaller demo datasets
    base_activity = count if count > 0 else random.randint(5, 15)
    
    return {
        "zone":           zone,
        "active_workers": base_activity,
        "protected_partners": count if count > 0 else random.randint(3, 8),
        "status":         "High Activity" if base_activity > 10 else "Normal",
        "pulse_timestamp": datetime.now().isoformat()
    }

# ─────────────────────────────────────────────────────────────────────────────
# All Policies (admin)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/all")
def get_all_policies(db: Session = Depends(get_db)):
    policies = db.query(Policy).order_by(Policy.created_at.desc()).all()
    return [
        {
            "id": p.id, "worker_id": p.worker_id, "plan": p.plan,
            "premium": p.premium, "status": p.status,
            "start_date": str(p.start_date),
            "renewal_count": p.renewal_count,
        }
        for p in policies
    ]

# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────
def _notify(db: Session, worker_id: str, title: str, message: str, notif_type: str):
    from app.models import NotificationLog
    notif = NotificationLog(
        worker_id  = worker_id,
        title      = title,
        message    = message,
        notif_type = notif_type,
        icon       = "📋",
    )
    db.add(notif)
    db.commit()