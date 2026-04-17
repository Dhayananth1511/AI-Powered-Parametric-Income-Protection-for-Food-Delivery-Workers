from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Worker, Claim, NotificationLog
from app.claims import run_claim_pipeline
from app.weather import fetch_weather, check_triggers
from app.trigger_monitor import (
    get_zone_status, simulate_disruption, clear_disruption,
    get_active_events, get_all_disruption_events_db
)
import uuid, json

router = APIRouter(prefix="/claims", tags=["claims"])

TRIGGER_MAP = {
    "rainfall":    {"type": "rainfall",    "value": 42.0, "label": "Heavy Rainfall",  "payout_type": "hourly",   "unit": "mm"},
    "temperature": {"type": "temperature", "value": 44.5, "label": "Extreme Heat",    "payout_type": "hourly",   "unit": "°C"},
    "aqi":         {"type": "aqi",         "value": 300,  "label": "Severe AQI",      "payout_type": "hourly",   "unit": "AQI"},
    "cyclone":     {"type": "cyclone",     "value": 1,    "label": "Cyclone Alert",   "payout_type": "full_cap", "unit": "alert"},
    "curfew":      {"type": "curfew",      "value": 1,    "label": "Curfew/Hartal",   "payout_type": "full_cap", "unit": "flag"},
}

class ClaimTrigger(BaseModel):
    worker_id:      str
    trigger_type:   str = "rainfall"
    disruption_hrs: float = 2.5
    simulate:       bool = True

class ClaimReview(BaseModel):
    claim_id: str
    action:   str   # "approve" | "reject"
    notes:    str = ""

class ZoneSimulate(BaseModel):
    zone:         str
    trigger_type: str = "rainfall"

class SandboxPayload(BaseModel):
    gps_distance: float
    motion_var: float
    signal_dbm: float
    latency: float
    gps_in_zone: bool
    accelerometer_ok: bool
    cell_tower_match: bool
    trust_score: float

# ─────────────────────────────────────────────────────────────────────────────
# Trigger / Simulate Claim
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/trigger")
async def trigger_claim(req: ClaimTrigger, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == req.worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")

    if worker.policy_status != "active":
        raise HTTPException(403, f"Claim rejected: Policy is {worker.policy_status or 'inactive'}. Please renew your coverage.")

    worker_dict = {
        "id": worker.id, "name": worker.name, "zone": worker.zone,
        "plan": worker.plan, "trust_score": worker.trust_score,
        "claims_total": worker.claims_total,
        "weekly_hrs_used": float(worker.weekly_hrs_used or 0.0),
    }

    # Use real OWM if not simulating
    if not req.simulate and req.trigger_type == "auto":
        from app.ml_engine import latest_telemetry
        lat, lon = None, None
        if req.worker_id in latest_telemetry:
            lat = latest_telemetry[req.worker_id].get("lat")
            lon = latest_telemetry[req.worker_id].get("lon")
            
        weather  = await fetch_weather(worker.zone, lat, lon)
        triggers = check_triggers(weather)
        if not triggers:
            return {
                "status":  "no_trigger",
                "message": "No disruption threshold crossed in your zone right now",
                "weather": weather
            }
        trigger = triggers[0]
    else:
        trigger = TRIGGER_MAP.get(req.trigger_type, TRIGGER_MAP["rainfall"])

    result = run_claim_pipeline(worker_dict, trigger, req.disruption_hrs, worker_dict["weekly_hrs_used"])

    # Explicitly set created_at from pipeline timestamp to avoid DB vs Python drift
    from datetime import datetime
    from zoneinfo import ZoneInfo
    created_at = datetime.fromisoformat(result["timestamp_ist"]) if "timestamp_ist" in result else datetime.now(ZoneInfo("Asia/Kolkata"))

    claim = Claim(
        id             = "CLM-" + uuid.uuid4().hex[:6].upper(),
        worker_id      = req.worker_id,
        trigger_type   = trigger["type"],
        trigger_value  = float(trigger["value"]),
        trigger_label  = trigger["label"],
        disruption_hrs = req.disruption_hrs,
        payout_amount  = result["payout"],
        fraud_score    = result["fraud"]["fraud_score"],
        status         = result["status"],
        razorpay_order_id = result.get("razorpay", {}).get("order_id", ""),
        notes          = result["fraud"]["decision"],
        pipeline_steps = json.dumps(result["steps"]),
        is_simulated   = req.simulate,
        created_at     = created_at,
    )
    db.add(claim)

    if result["status"] in ["approved", "manual_review"]:
        worker.sim_payouts       = (worker.sim_payouts or 0) + result["payout"]
        worker.claims_total      = (worker.claims_total or 0) + 1
        worker.claims_approved   = (worker.claims_approved or 0) + 1
        worker.weekly_hrs_used   = (worker.weekly_hrs_used or 0) + result.get("hrs_added", 0)
        worker.trust_score       = min(100, (worker.trust_score or 40) + 2)
        worker.earnings_protected = (worker.earnings_protected or 0) + result["payout"]
        
        if result["status"] == "approved":
            from app.sms_engine import send_sms_notification
            send_sms_notification(
                to_phone=worker.phone,
                message=f"ZenVyte GigPulse: Claim for {trigger['label']} Auto-Approved! ₹{result['payout']} has been credited."
            )
            
    elif result["status"] == "rejected":
        worker.claims_rejected  = (worker.claims_rejected or 0) + 1
        worker.trust_score      = max(0, (worker.trust_score or 40) - 3)

    db.commit()
    return {**result, "claim_id": claim.id}

# ─────────────────────────────────────────────────────────────────────────────
# Auto Check — Real trigger detection for worker's zone
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/auto-check/{worker_id}")
async def auto_check(worker_id: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(404, "Worker not found")
        
    from app.ml_engine import latest_telemetry
    lat, lon = None, None
    if worker_id in latest_telemetry:
        lat = latest_telemetry[worker_id].get("lat")
        lon = latest_telemetry[worker_id].get("lon")
        
    weather  = await fetch_weather(worker.zone, lat, lon)
    triggers = check_triggers(weather)
    zone_status = get_zone_status(worker.zone)
    return {
        "worker_id":    worker_id,
        "zone":         worker.zone,
        "weather":      weather,
        "triggers":     triggers,
        "zone_status":  zone_status,
        "payout_active": len(triggers) > 0 or zone_status["payout_active"],
    }

# ─────────────────────────────────────────────────────────────────────────────
# Zone Status — Live trigger state for a zone
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/zone-status/{zone}")
def zone_status(zone: str):
    return get_zone_status(zone)

# ─────────────────────────────────────────────────────────────────────────────
# Simulate Zone Disruption — Auto-triggers payouts for all workers in zone
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/sandbox/evaluate")
def sandbox_evaluate(req: SandboxPayload):
    from app.ml_engine import compute_fraud_score
    worker_data = {
        "id": "SANDBOX_MOCK_WORKER",
        "trust_score": req.trust_score,
        "claims_total": 0,
        "sandbox_overrides": {
            "gps_distance": req.gps_distance,
            "motion_var": req.motion_var,
            "signal_dbm": req.signal_dbm,
            "latency": req.latency
        }
    }
    
    # We also need to hack the base signals before compute_fraud_score evaluates them
    # But compute_fraud_score computes them dynamically based on trust score.
    # The sandbox passes exact telemetry which our modified ml_engine parses directly.
    return compute_fraud_score(worker_data)

# ─────────────────────────────────────────────────────────────────────────────
# Simulate Zone Disruption — Auto-triggers payouts for all workers in zone
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/zone-simulate")
def zone_simulate(req: ZoneSimulate, db: Session = Depends(get_db)):
    # 1. Register disruption event
    disruption = simulate_disruption(req.zone, req.trigger_type)
    trigger = disruption["trigger"]

    # 2. Find all active workers in this zone with an ACTIVE policy
    workers = db.query(Worker).filter(
        Worker.zone == req.zone,
        Worker.is_active == True,
        Worker.policy_status == "active"
    ).all()

    payout_results = []
    total_payout = 0.0

    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    base_time = datetime.now(ZoneInfo("Asia/Kolkata"))

    # 3. Run claim pipeline for each worker (auto zero-touch payout)
    for i, worker in enumerate(workers):
        worker_dict = {
            "id": worker.id, "name": worker.name, "zone": worker.zone,
            "plan": worker.plan, "trust_score": worker.trust_score,
            "claims_total": worker.claims_total,
            "weekly_hrs_used": float(worker.weekly_hrs_used or 0.0),
        }
        # Default disruption hours by plan
        plan_hrs = {"starter": 2.0, "basic": 2.5, "standard": 3.0, "premium": 4.0, "elite": 5.0}
        disruption_hrs = plan_hrs.get(worker.plan, 3.0)

        result = run_claim_pipeline(worker_dict, trigger, disruption_hrs, worker_dict["weekly_hrs_used"])
        
        # Explicitly set created_at with slight increment so claims in a zone simulation have unique times
        created_at = base_time + timedelta(seconds=i)
        result["timestamp_ist"] = created_at.isoformat()

        claim = Claim(
            id              = "CLM-" + uuid.uuid4().hex[:6].upper(),
            worker_id       = worker.id,
            trigger_type    = trigger["type"],
            trigger_value   = float(trigger["value"]),
            trigger_label   = trigger["label"],
            disruption_hrs  = disruption_hrs,
            payout_amount   = result["payout"],
            fraud_score     = result["fraud"]["fraud_score"],
            status          = result["status"],
            razorpay_order_id = result.get("razorpay", {}).get("order_id", ""),
            notes           = f"Auto-triggered zone disruption: {req.zone}",
            pipeline_steps  = json.dumps(result["steps"]),
            is_simulated    = True,
            created_at      = created_at,
        )
        db.add(claim)

        if result["status"] in ["approved", "manual_review"]:
            worker.sim_payouts       = (worker.sim_payouts or 0) + result["payout"]
            worker.claims_total      = (worker.claims_total or 0) + 1
            worker.claims_approved   = (worker.claims_approved or 0) + 1
            worker.weekly_hrs_used   = (worker.weekly_hrs_used or 0) + result.get("hrs_added", 0)
            worker.trust_score       = min(100, (worker.trust_score or 40) + 1)
            worker.earnings_protected = (worker.earnings_protected or 0) + result["payout"]
            total_payout += result["payout"]
        elif result["status"] == "rejected":
            worker.claims_rejected = (worker.claims_rejected or 0) + 1

        # 4. Push payout notification to each worker
        if result["status"] == "approved":
            notif_msg = (
                f"Auto-payout of ₹{result['payout']} credited via zero-touch pipeline "
                f"due to {trigger['label']} in {req.zone}."
            )
            notif_icon = {"rainfall":"🌧️","temperature":"🔥","aqi":"💨","cyclone":"🌀","curfew":"🚫"}.get(trigger["type"],"⚡")
            notif = NotificationLog(
                worker_id  = worker.id,
                title      = f"💸 Auto-Payout: ₹{result['payout']} Credited!",
                message    = notif_msg,
                notif_type = "payout_credited",
                amount     = result["payout"],
                icon       = notif_icon,
            )
            db.add(notif)
            
            from app.sms_engine import send_sms_notification
            send_sms_notification(
                to_phone=worker.phone,
                message=notif_msg
            )
            
        elif result["status"] == "manual_review":
            notif = NotificationLog(
                worker_id  = worker.id,
                title      = f"⏳ Claim Under Review — {trigger['label']}",
                message    = f"Your zone disruption claim is under manual review. Expected resolution in 2hrs.",
                notif_type = "claim_submitted",
                icon       = "⏳",
            )
            db.add(notif)

        payout_results.append({
            "worker_id":   worker.id,
            "worker_name": worker.name,
            "plan":        worker.plan,
            "payout":      result["payout"],
            "status":      result["status"],
            "claim_id":    claim.id,
        })

    db.commit()

    return {
        **disruption,
        "auto_payouts_triggered": len(payout_results),
        "workers_affected":       len(workers),
        "total_payout_amount":    total_payout,
        "payout_results":         payout_results,
        "message": f"Zone disruption confirmed! Auto-payout pipeline triggered for {len(workers)} workers in {req.zone}.",
    }

# ─────────────────────────────────────────────────────────────────────────────
# Clear Zone Disruption
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/zone-clear/{zone}")
def zone_clear(zone: str):
    return clear_disruption(zone)

# ─────────────────────────────────────────────────────────────────────────────
# Active Disruption Events
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/disruption-events")
def disruption_events():
    return {
        "active_in_memory": get_active_events(),
        "recent_db":        get_all_disruption_events_db(20),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Claims by Worker
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/worker/{worker_id}")
def get_claims(worker_id: str, db: Session = Depends(get_db)):
    claims = (db.query(Claim)
              .filter(Claim.worker_id == worker_id)
              .order_by(Claim.created_at.desc())
              .all())
    return [
        {
            "id":               c.id,
            "trigger_type":     c.trigger_type,
            "trigger_label":    c.trigger_label,
            "trigger_value":    c.trigger_value,
            "disruption_hrs":   c.disruption_hrs,
            "payout_amount":    c.payout_amount,
            "fraud_score":      c.fraud_score,
            "status":           c.status,
            "razorpay_order_id":c.razorpay_order_id,
            "is_simulated":     c.is_simulated,
            "created_at":       str(c.created_at),
        }
        for c in claims
    ]

# ─────────────────────────────────────────────────────────────────────────────
# All Claims (admin)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/all")
def get_all_claims(db: Session = Depends(get_db)):
    claims = db.query(Claim).order_by(Claim.created_at.desc()).all()
    workers = {w.id: w.name for w in db.query(Worker).all()}
    return [
        {
            "id":               c.id,
            "worker_id":        c.worker_id,
            "worker_name":      workers.get(c.worker_id, "Unknown"),
            "trigger_type":     c.trigger_type,
            "trigger_label":    c.trigger_label,
            "payout_amount":    c.payout_amount,
            "fraud_score":      c.fraud_score,
            "status":           c.status,
            "is_simulated":     c.is_simulated,
            "created_at":       str(c.created_at),
            "razorpay_order_id":c.razorpay_order_id,
        }
        for c in claims
    ]

# ─────────────────────────────────────────────────────────────────────────────
# Review Claim (manual approve/reject)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/review")
def review_claim(req: ClaimReview, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == req.claim_id).first()
    if not claim:
        raise HTTPException(404, "Claim not found")

    new_status = "approved" if req.action == "approve" else "rejected"
    claim.status = new_status
    claim.notes  = req.notes

    worker = db.query(Worker).filter(Worker.id == claim.worker_id).first()
    if worker:
        if new_status == "approved":
            worker.sim_payouts      = (worker.sim_payouts or 0) + claim.payout_amount
            worker.claims_approved  = (worker.claims_approved or 0) + 1
            worker.earnings_protected = (worker.earnings_protected or 0) + claim.payout_amount
            # Send notification
            from app.models import NotificationLog
            notif = NotificationLog(
                worker_id  = claim.worker_id,
                title      = f"✅ Claim Approved — ₹{claim.payout_amount}",
                message    = f"Manual review approved · {claim.trigger_label or claim.trigger_type} · ₹{claim.payout_amount} credited",
                notif_type = "payout_credited",
                amount     = claim.payout_amount,
                icon       = "✅",
            )
            db.add(notif)
            
            from app.sms_engine import send_sms_notification
            send_sms_notification(
                to_phone=worker.phone,
                message=f"ZenVyte GigPulse: Your claim for {claim.trigger_label or claim.trigger_type} was manually approved! ₹{claim.payout_amount} credited."
            )
        else:
            worker.claims_rejected = (worker.claims_rejected or 0) + 1

    db.commit()
    return {"success": True, "claim_id": claim.id, "status": new_status}

# ─────────────────────────────────────────────────────────────────────────────
# Claims Pipeline Summary (admin)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/pipeline/summary")
def pipeline_summary(db: Session = Depends(get_db)):
    claims = db.query(Claim).all()
    workers = {w.id: w.name for w in db.query(Worker).all()}

    def enrich(c):
        return {
            "id":            c.id,
            "worker_id":     c.worker_id,
            "worker_name":   workers.get(c.worker_id, "Unknown"),
            "trigger_type":  c.trigger_type,
            "trigger_label": c.trigger_label,
            "payout_amount": c.payout_amount,
            "fraud_score":   c.fraud_score,
            "status":        c.status,
            "is_simulated":  c.is_simulated,
            "created_at":    str(c.created_at),
        }

    return {
        "approved":         [enrich(c) for c in claims if c.status == "approved"],
        "manual_review":    [enrich(c) for c in claims if c.status == "manual_review"],
        "rejected":         [enrich(c) for c in claims if c.status == "rejected"],
        "total_approved":   sum(1 for c in claims if c.status == "approved"),
        "total_review":     sum(1 for c in claims if c.status == "manual_review"),
        "total_rejected":   sum(1 for c in claims if c.status == "rejected"),
        "total_payout":     sum(c.payout_amount for c in claims if c.status == "approved"),
    }