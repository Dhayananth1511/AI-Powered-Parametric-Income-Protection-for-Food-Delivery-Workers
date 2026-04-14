import sys
import os
from pathlib import Path
import io

# Fix sys.path if run directly as python app/main.py
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Fix stdout encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.security import require_role
from app.database import engine, Base, SessionLocal
from app.models import Worker, Admin, Policy, Claim, WeatherLog, NotificationLog
from app import routes_auth, routes_policy, routes_claims, routes_weather
from app import routes_kyc, routes_notifications, routes_payments
from app.ml_engine import compute_risk_score, recommend_plan, calculate_dynamic_premium
from app.trigger_monitor import get_active_events, get_all_disruption_events_db
from app.scheduler import initialize_scheduler, stop_scheduler as stop_bg_scheduler, get_scheduler_status
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import os
import logging

# ─────────────────────────────────────────────────────────────────────────────
# Configure Logging
# ─────────────────────────────────────────────────────────────────────────────
log_handlers = [logging.StreamHandler()]
if os.getenv("ENABLE_FILE_LOGGING", "").lower() in {"1", "true", "yes", "on"}:
    log_handlers.append(logging.FileHandler("gigpulse.log", encoding='utf-8'))

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "ERROR").upper(), logging.ERROR),
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=log_handlers
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Create all tables
# ─────────────────────────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

from sqlalchemy import text
from datetime import timedelta

_POLICY_MIGRATIONS = [
    "ALTER TABLE workers ADD COLUMN bank_upi_id VARCHAR",
    "ALTER TABLE workers ADD COLUMN plan_expiry_notified BOOLEAN DEFAULT 0",
    "ALTER TABLE workers ADD COLUMN policy_start_date DATETIME",
    "ALTER TABLE workers ADD COLUMN policy_expiry_date DATETIME",
    "ALTER TABLE workers ADD COLUMN policy_status VARCHAR DEFAULT 'active'",
]
with engine.connect() as conn:
    for sql in _POLICY_MIGRATIONS:
        try:
            conn.execute(text(sql))
            conn.commit()
        except Exception:
            pass

# Seed policy dates for workers that have none
with engine.connect() as conn:
    try:
        now = datetime.now()
        week = timedelta(days=7)
        conn.execute(text(
            "UPDATE workers SET policy_start_date=:s, policy_expiry_date=:e, policy_status='active' "
            "WHERE policy_start_date IS NULL"
        ), {"s": now.isoformat(), "e": (now + week).isoformat()})
        conn.commit()
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ZenVyte GigPulse API",
    description="AI-Powered Parametric Income Protection for Food Delivery Workers — Phase 2 (PRODUCTION READY)",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─────────────────────────────────────────────────────────────────────────────
# Security: Proper CORS Configuration
# ─────────────────────────────────────────────────────────────────────────────
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Fixed: not "all origins"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# Security: Rate Limiting Middleware
# ─────────────────────────────────────────────────────────────────────────────
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address

    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
except ImportError:
    app.state.limiter = None

# ─────────────────────────────────────────────────────────────────────────────
# Register Routers
# ─────────────────────────────────────────────────────────────────────────────
app.include_router(routes_auth.router)
app.include_router(routes_policy.router)
app.include_router(routes_claims.router)
app.include_router(routes_weather.router)
app.include_router(routes_kyc.router)
app.include_router(routes_notifications.router)
app.include_router(routes_payments.router)  # Phase 2A: Payment integration

# Static Frontend (Mount after all routes)
static_path = os.path.join(os.path.dirname(__file__), "..", "static")

# ─────────────────────────────────────────────────────────────────────────────
# Seed Database (idempotent)
# ─────────────────────────────────────────────────────────────────────────────
def seed_db():
    if os.getenv("SKIP_SEEDING", "").lower() in {"1", "true", "yes"}:
        logger.info("⏭️ Skipping database seeding per environment variable.")
        return

    db: Session = SessionLocal()
    try:
        if db.query(Worker).count() == 0:
            from app.security import hash_password
            workers = [
                Worker(
                    id="WKR-4821", name="Ravi Kumar", phone="+91 98765 43210",
                    email="ravi.kumar@swiggy.in", password=hash_password("demo1234"),
                    platform="Swiggy", zone="Velachery, Chennai", pincode="600042",
                    plan="standard", risk_score=0.58, trust_score=92,
                    payouts=640, sim_payouts=1240, claims_total=12,
                    claims_approved=10, claims_rejected=2,
                    aadhaar_verified=True, earnings_protected=1640,
                ),
                Worker(
                    id="WKR-3302", name="Arjun Raj", phone="+91 90123 45678",
                    email="arjun.raj@zomato.in", password=hash_password("demo1234"),
                    platform="Zomato", zone="Marina Beach, Chennai", pincode="600005",
                    plan="elite", risk_score=0.85, trust_score=88,
                    payouts=1200, sim_payouts=2430, claims_total=18,
                    claims_approved=15, claims_rejected=3,
                    aadhaar_verified=True, earnings_protected=3630,
                ),
                Worker(
                    id="WKR-7741", name="Suresh Murugan", phone="+91 87654 32109",
                    email="suresh.m@swiggy.in", password=hash_password("demo1234"),
                    platform="Swiggy", zone="T. Nagar, Chennai", pincode="600017",
                    plan="basic", risk_score=0.45, trust_score=61,
                    payouts=270, sim_payouts=540, claims_total=6,
                    claims_approved=5, claims_rejected=1,
                    aadhaar_verified=True, earnings_protected=810,
                ),
                Worker(
                    id="WKR-5593", name="Priya Devi", phone="+91 76543 21098",
                    email="priya.d@zomato.in", password=hash_password("demo1234"),
                    platform="Zomato", zone="Adyar, Chennai", pincode="600020",
                    plan="premium", risk_score=0.72, trust_score=78,
                    payouts=900, sim_payouts=1350, claims_total=10,
                    claims_approved=8, claims_rejected=2,
                    aadhaar_verified=True, earnings_protected=2250,
                ),
                Worker(
                    id="WKR-8847", name="Karthik Selvam", phone="+91 65432 10987",
                    email="karthik.s@swiggy.in", password=hash_password("demo1234"),
                    platform="Swiggy", zone="Guindy, Chennai", pincode="600032",
                    plan="starter", risk_score=0.32, trust_score=45,
                    payouts=105, sim_payouts=210, claims_total=3,
                    claims_approved=2, claims_rejected=1,
                    aadhaar_verified=False, earnings_protected=315,
                ),
            ]
            for w in workers:
                db.add(w)

        if db.query(Admin).count() == 0:
            from app.security import hash_password
            admins = [
                Admin(
                    id="ADM-001", name="Karthik Sundaram",
                    email="admin@digit.com", password=hash_password("admin123"),
                    org="Digit Insurance Pvt Ltd", designation="Portfolio Manager",
                ),
                Admin(
                    id="ADM-002", name="Priya Nair",
                    email="ops@gigpulse.in", password=hash_password("admin123"),
                    org="ZenVyte GigPulse Platform Admin", designation="Platform Admin",
                ),
            ]
            for a in admins:
                db.add(a)

        # Seed some claims if none exist
        if db.query(Claim).count() == 0:
            import uuid
            seed_claims = [
                Claim(id="CLM-A001", worker_id="WKR-4821", trigger_type="rainfall",
                      trigger_label="Heavy Rainfall", trigger_value=42.0,
                      disruption_hrs=5.0, payout_amount=300.0, fraud_score=14,
                      status="approved", razorpay_order_id="order_mock_001", is_simulated=True),
                Claim(id="CLM-A002", worker_id="WKR-3302", trigger_type="cyclone",
                      trigger_label="Cyclone Alert", trigger_value=1.0,
                      disruption_hrs=7.0, payout_amount=630.0, fraud_score=8,
                      status="approved", razorpay_order_id="order_mock_002", is_simulated=True),
                Claim(id="CLM-A003", worker_id="WKR-7741", trigger_type="temperature",
                      trigger_label="Extreme Heat", trigger_value=44.5,
                      disruption_hrs=4.0, payout_amount=180.0, fraud_score=22,
                      status="approved", razorpay_order_id="order_mock_003", is_simulated=True),
                Claim(id="CLM-A004", worker_id="WKR-5593", trigger_type="aqi",
                      trigger_label="Severe AQI", trigger_value=320.0,
                      disruption_hrs=3.0, payout_amount=225.0, fraud_score=19,
                      status="approved", razorpay_order_id="order_mock_004", is_simulated=True),
                Claim(id="CLM-M001", worker_id="WKR-4821", trigger_type="rainfall",
                      trigger_label="Heavy Rainfall", trigger_value=36.0,
                      disruption_hrs=2.5, payout_amount=150.0, fraud_score=45,
                      status="manual_review", razorpay_order_id="", is_simulated=True),
                Claim(id="CLM-M002", worker_id="WKR-8847", trigger_type="temperature",
                      trigger_label="Extreme Heat", trigger_value=43.5,
                      disruption_hrs=2.0, payout_amount=70.0, fraud_score=52,
                      status="manual_review", razorpay_order_id="", is_simulated=True),
                Claim(id="CLM-R001", worker_id="WKR-7741", trigger_type="rainfall",
                      trigger_label="Heavy Rainfall", trigger_value=38.0,
                      disruption_hrs=3.0, payout_amount=0.0, fraud_score=82,
                      status="rejected", razorpay_order_id="", is_simulated=True),
            ]
            for c in seed_claims:
                db.add(c)

        db.commit()
        logger.info("✅ Database seeded successfully")
    except Exception as e:
        logger.error(f"❌ Seed error: {e}")
        db.rollback()
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    """Start background jobs on application startup."""
    # Seed database (checks SKIP_SEEDING inside)
    seed_db()
    # Start the consolidated scheduler
    initialize_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop background jobs on application shutdown."""
    stop_bg_scheduler()

# ─────────────────────────────────────────────────────────────────────────────
# Root & Health
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api")
def api_root():
    return {
        "app":     "ZenVyte GigPulse API v2.0",
        "status":  "running",
        "team":    "ZenVyte",
        "phase":   "Phase 2 - Automation & Protection",
        "docs":    "/docs",
    }

@app.get("/health")
def health():
    return {"status": "healthy", "version": "2.1.0", "python": "3.13"}

@app.get("/scheduler/status")
def get_scheduler_info():
    """Get background job scheduler status."""
    return get_scheduler_status()

# ─────────────────────────────────────────────────────────────────────────────
# Admin Stats (7 KPIs)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/admin/stats", dependencies=[Depends(require_role(["admin"]))])
def admin_stats():
    db: Session = SessionLocal()
    try:
        workers = db.query(Worker).all()
        claims  = db.query(Claim).all()
        plan_prices = {"starter":55,"basic":70,"standard":90,"premium":115,"elite":135}

        total_premium = sum(plan_prices.get(w.plan, 90) for w in workers)
        total_payouts = sum((w.payouts or 0) + (w.sim_payouts or 0) for w in workers)
        total_earnings_protected = sum(w.earnings_protected or 0 for w in workers)

        approved     = [c for c in claims if c.status == "approved"]
        rejected     = [c for c in claims if c.status == "rejected"]
        review       = [c for c in claims if c.status == "manual_review"]
        loss_ratio   = round((total_payouts / (total_premium * 52) * 100), 1) if total_premium > 0 else 0

        plan_dist = {}
        for w in workers:
            plan_dist[w.plan] = plan_dist.get(w.plan, 0) + 1

        today = date.today()
        new_today = sum(
            1 for w in workers
            if w.joined and w.joined.date() == today
        )

        aadhaar_verified = sum(1 for w in workers if w.aadhaar_verified)
        avg_trust = round(sum(w.trust_score or 40 for w in workers) / len(workers), 1) if workers else 0

        return {
            "policies":               len(workers),
            "weekly_premium":         total_premium,
            "total_payouts":          total_payouts,
            "platform_fee":           round(total_premium * 0.05, 1),
            "total_claims":           len(claims),
            "approved_claims":        len(approved),
            "rejected_claims":        len(rejected),
            "review_claims":          len(review),
            "loss_ratio":             loss_ratio,
            "plan_breakdown":         plan_dist,
            "new_today":              new_today,
            "aadhaar_verified":       aadhaar_verified,
            "avg_trust_score":        avg_trust,
            "total_earnings_protected": total_earnings_protected,
            "active_disruptions":     len(get_active_events()),
        }
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Admin — Workers List
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/workers")
def get_workers():
    db = SessionLocal()
    try:
        workers = db.query(Worker).all()
        return {
            "workers": [
                {
                    "id": w.id, "name": w.name, "phone": w.phone,
                    "email": w.email, "zone": w.zone, "plan": w.plan,
                    "risk_score": w.risk_score, "trust_score": w.trust_score,
                    "payouts": w.payouts, "sim_payouts": w.sim_payouts,
                    "claims_total": w.claims_total,
                    "claims_approved": w.claims_approved,
                    "claims_rejected": w.claims_rejected,
                    "platform": w.platform,
                    "joined": str(w.joined) if w.joined else None,
                    "aadhaar_verified": w.aadhaar_verified,
                    "earnings_protected": w.earnings_protected,
                    "role": "worker",
                }
                for w in workers
            ]
        }
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Admin — Admins List
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/admins")
def get_admins():
    db = SessionLocal()
    try:
        admins = db.query(Admin).all()
        return {
            "admins": [
                {
                    "id": a.id, "name": a.name, "email": a.email,
                    "org": a.org, "designation": a.designation,
                    "joined": str(a.joined) if a.joined else None,
                    "role": "admin",
                }
                for a in admins
            ]
        }
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Admin — Disruption Monitor
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/admin/disruption-monitor")
def disruption_monitor():
    return {
        "active_events": get_active_events(),
        "recent_events": get_all_disruption_events_db(10),
        "total_active":  len(get_active_events()),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Worker Update (PATCH — safe fields only)
# ─────────────────────────────────────────────────────────────────────────────
SAFE_UPDATE_FIELDS = {"plan", "sim_payouts", "weekly_hrs_used", "trust_score", "is_active"}

@app.put("/workers/{worker_id}")
def update_worker_data(worker_id: str, patch: dict):
    db = SessionLocal()
    try:
        w = db.query(Worker).filter(Worker.id == worker_id).first()
        if not w:
            return {"success": False, "error": "Worker not found"}
        for key, value in patch.items():
            if key in SAFE_UPDATE_FIELDS and hasattr(w, key):
                setattr(w, key, value)
        db.commit()
        return {"success": True, "worker_id": worker_id}
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Worker Telemetry Cache (Hardware Sensor Heartbeat)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/workers/{worker_id}/telemetry")
def update_worker_telemetry(worker_id: str, telemetry: dict):
    from app.ml_engine import latest_telemetry
    latest_telemetry[worker_id] = telemetry
    return {"success": True, "recorded": True}

from pydantic import BaseModel
class ShiftRequest(BaseModel):
    is_online: bool

@app.put("/workers/{worker_id}/shift")
def toggle_worker_shift(worker_id: str, req: ShiftRequest):
    db: Session = SessionLocal()
    try:
        from app.models import Worker
        w = db.query(Worker).filter(Worker.id == worker_id).first()
        if w:
            w.is_online = req.is_online
            db.commit()
            return {"success": True, "is_online": w.is_online}
        return {"success": False, "error": "Worker not found"}
    finally:
        db.close()

@app.get("/admin/telemetry")
def get_all_telemetry():
    from app.ml_engine import latest_telemetry
    db: Session = SessionLocal()
    try:
        from app.models import Worker
        # Append is_online status directly into telemetry packet for admin to know state
        workers = db.query(Worker).all()
        state_map = { w.id: w.is_online for w in workers }
        for k, v in latest_telemetry.items():
            if isinstance(v, dict):
                v["is_online"] = state_map.get(k, False)
        return {"telemetry": latest_telemetry}
    finally:
        db.close()

@app.get("/workers/{worker_id}/earnings-history")
def get_earnings_history(worker_id: str):
    db = SessionLocal()
    try:
        claims = db.query(Claim).filter(Claim.worker_id == worker_id, Claim.status == "approved").order_by(Claim.created_at.asc()).all()
        return {
            "success": True,
            "claims": [{"amount": c.payout_amount, "date": str(c.created_at)} for c in claims]
        }
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Policy Lifecycle — Active / Expired / Renewal
# ─────────────────────────────────────────────────────────────────────────────
PLAN_WEEKLY_PREMIUMS = {"starter": 55, "basic": 70, "standard": 90, "premium": 115, "elite": 135}

def _policy_status_for(w) -> dict:
    """Compute real-time policy status for a worker."""
    now = datetime.now()
    expiry = w.policy_expiry_date
    start  = w.policy_start_date

    if not expiry:
        status = w.policy_status or "active"
        days_left = None
        alert = None
    else:
        days_left = (expiry - now).days
        hours_left = (expiry - now).total_seconds() / 3600

        if now > expiry:
            status = "expired"
            alert  = "🚨 Policy expired — coverage suspended"
        elif days_left <= 1:
            status = "grace_period"
            alert  = f"⚠️ Policy expires in {int(hours_left)} hours — renew now!"
        elif days_left <= 2:
            status = "expiring_soon"
            alert  = f"⏰ Policy renews in {days_left} days"
        else:
            status = "active"
            alert  = None

    return {
        "policy_status":  status,
        "policy_start":   start.isoformat() if start else None,
        "policy_expiry":  expiry.isoformat() if expiry else None,
        "days_remaining": days_left,
        "next_renewal":   expiry.isoformat() if expiry else None,
        "weekly_premium": PLAN_WEEKLY_PREMIUMS.get(w.plan, 90),
        "alert":          alert,
        "is_covered":     status in ("active", "expiring_soon", "grace_period"),
    }

@app.get("/workers/{worker_id}/policy-status")
def get_worker_policy_status(worker_id: str):
    """Get real-time policy status, renewal date, and alert for a worker."""
    db = SessionLocal()
    try:
        w = db.query(Worker).filter(Worker.id == worker_id).first()
        if not w:
            raise HTTPException(status_code=404, detail="Worker not found")
        return {"success": True, "worker_id": worker_id, **_policy_status_for(w)}
    finally:
        db.close()

@app.post("/workers/{worker_id}/renew-policy")
def renew_worker_policy(worker_id: str):
    """Manually renew a worker's policy for another 7 days."""
    db = SessionLocal()
    try:
        w = db.query(Worker).filter(Worker.id == worker_id).first()
        if not w:
            raise HTTPException(status_code=404, detail="Worker not found")

        now = datetime.now()
        # If already active/expiring_soon, extend from current expiry; else from now
        base = w.policy_expiry_date if (w.policy_expiry_date and w.policy_expiry_date > now) else now
        new_expiry = base + timedelta(days=7)

        w.policy_start_date = now
        w.policy_expiry_date = new_expiry
        w.policy_status = "active"
        w.plan_expiry_notified = False
        w.is_active = True

        # Send renewal notification
        import uuid as _uuid
        from app.models import NotificationLog
        notif = NotificationLog(
            id=f"NTF-{_uuid.uuid4().hex[:8].upper()}",
            worker_id=worker_id,
            title="✅ Policy Renewed",
            message=f"Your {w.plan.capitalize()} plan has been renewed until {new_expiry.strftime('%d %b %Y')}. Stay covered!",
            notif_type="plan_change",
            icon="✅"
        )
        db.add(notif)
        db.commit()

        logger.info(f"✅ Policy renewed for {worker_id} → expires {new_expiry.date()}")
        return {
            "success": True,
            "worker_id": worker_id,
            "new_expiry": new_expiry.isoformat(),
            "message": f"Policy renewed until {new_expiry.strftime('%d %b %Y')}"
        }
    finally:
        db.close()

@app.get("/admin/policy-overview")
def get_policy_overview():
    """Admin view: all workers with policy status, expiry dates, and alerts."""
    db = SessionLocal()
    try:
        workers = db.query(Worker).all()
        result = []
        counts = {"active": 0, "expiring_soon": 0, "grace_period": 0, "expired": 0}
        for w in workers:
            ps = _policy_status_for(w)
            counts[ps["policy_status"]] = counts.get(ps["policy_status"], 0) + 1
            result.append({
                "id": w.id, "name": w.name, "plan": w.plan,
                "zone": w.zone, "platform": w.platform,
                **ps
            })
        # Sort: expired first, then grace_period, then expiring_soon, then active
        order = {"expired": 0, "grace_period": 1, "expiring_soon": 2, "active": 3}
        result.sort(key=lambda x: order.get(x["policy_status"], 4))
        return {"workers": result, "summary": counts, "total": len(result)}
    finally:
        db.close()

@app.post("/admin/policy-lifecycle-check")
def run_policy_lifecycle_check():
    """Manually trigger the weekly policy expiry check (also runs automatically)."""
    from app.scheduler import job_policy_lifecycle
    job_policy_lifecycle()
    return {"success": True, "message": "Policy lifecycle check completed"}

# ─────────────────────────────────────────────────────────────────────────────
@app.get("/ml/zones")
def get_zones():
    from app.ml_engine import get_all_zones, get_zone_categories
    return {
        "zones":      get_all_zones(),
        "categories": get_zone_categories(),
        "total":      len(get_all_zones()),
    }

@app.get("/ml/risk/{zone}")
def get_zone_risk(zone: str, month: int = None):
    from app.ml_engine import zone_risk_breakdown
    if month is None:
        month = datetime.now().month
    return zone_risk_breakdown(zone, month)

@app.get("/ml/forecast/{zone}")
def get_forecast(zone: str):
    from app.ml_engine import predict_disruption_probability
    return predict_disruption_probability(zone)

@app.get("/ml/loss-ratio/{plan}")
def get_loss_ratio(plan: str, disruption_hrs: float = 52.5):
    from app.ml_engine import calculate_loss_ratio
    return calculate_loss_ratio(plan, disruption_hrs)

# ─────────────────────────────────────────────────────────────────────────────
# Phase 3: Compliance Center — Market Crash Defense
# ─────────────────────────────────────────────────────────────────────────────

# In-memory compliance state (survives process restarts via seeding below)
_COMPLIANCE_STATE = {
    "market_crash_active": False,
    "new_premium_cap":     None,   # e.g. 90 rupees if regulator forces a cap
    "new_payout_cap":      None,   # e.g. 300 rupees
    "sabotage_shield":     False,  # unlockable DC purchase
    "freeze_new_policies": False,
    "emergency_reserve_pct": 5.0,  # % of premiums held in reserve
    "compliance_notes":    [],
    "last_updated":        None,
}

from pydantic import BaseModel as _BM
class CompliancePatch(_BM):
    market_crash_active: bool = None
    new_premium_cap: float = None
    new_payout_cap: float = None
    sabotage_shield: bool = None
    freeze_new_policies: bool = None
    emergency_reserve_pct: float = None
    note: str = None

@app.get("/admin/compliance")
def get_compliance_state():
    """Get the current Phase 3 compliance / market crash state."""
    return _COMPLIANCE_STATE

@app.post("/admin/compliance")
def update_compliance_state(patch: CompliancePatch):
    """Update compliance parameters in real-time (Market Crash response)."""
    if patch.market_crash_active is not None:
        _COMPLIANCE_STATE["market_crash_active"] = patch.market_crash_active
    if patch.new_premium_cap is not None:
        _COMPLIANCE_STATE["new_premium_cap"] = patch.new_premium_cap
    if patch.new_payout_cap is not None:
        _COMPLIANCE_STATE["new_payout_cap"] = patch.new_payout_cap
    if patch.sabotage_shield is not None:
        _COMPLIANCE_STATE["sabotage_shield"] = patch.sabotage_shield
    if patch.freeze_new_policies is not None:
        _COMPLIANCE_STATE["freeze_new_policies"] = patch.freeze_new_policies
    if patch.emergency_reserve_pct is not None:
        _COMPLIANCE_STATE["emergency_reserve_pct"] = patch.emergency_reserve_pct
    if patch.note:
        _COMPLIANCE_STATE["compliance_notes"].append({
            "text": patch.note,
            "at": datetime.now().isoformat()
        })
    _COMPLIANCE_STATE["last_updated"] = datetime.now().isoformat()
    logger.info(f"🚨 Compliance state updated: crash={_COMPLIANCE_STATE['market_crash_active']}")
    return {"success": True, "state": _COMPLIANCE_STATE}

@app.get("/admin/loss-ratio-trend")
def get_loss_ratio_trend():
    """Return week-by-week loss ratio trend for the admin dashboard chart."""
    from app.ml_engine import PLAN_BASE
    db = SessionLocal()
    try:
        claims = db.query(Claim).filter(Claim.status == "approved").order_by(Claim.created_at.asc()).all()
        workers = db.query(Worker).all()
        plan_prices = {p: PLAN_BASE[p]["premium"] for p in PLAN_BASE}

        # Group claims by ISO week
        from collections import defaultdict
        weeks: dict = defaultdict(lambda: {"payouts": 0.0, "premium": 0.0})
        weekly_premium = sum(plan_prices.get(w.plan, 90) for w in workers)

        for c in claims:
            if c.created_at:
                week_key = c.created_at.strftime("%Y-W%W")
                weeks[week_key]["payouts"] += c.payout_amount or 0

        for wk in weeks:
            weeks[wk]["premium"] = weekly_premium
            weeks[wk]["loss_ratio"] = round(
                weeks[wk]["payouts"] / weekly_premium * 100, 1
            ) if weekly_premium > 0 else 0.0

        sorted_weeks = sorted(weeks.items())
        return {
            "weeks": [
                {"week": w, "payouts": v["payouts"], "premium": v["premium"], "loss_ratio": v["loss_ratio"]}
                for w, v in sorted_weeks
            ],
            "plans": {p: {"normal_lr": round(PLAN_BASE[p]["rate"]*52.5/(PLAN_BASE[p]["premium"]*52)*100,1),
                          "monsoon_lr": round(PLAN_BASE[p]["rate"]*73.5/(PLAN_BASE[p]["premium"]*52)*100,1)}
                     for p in PLAN_BASE}
        }
    finally:
        db.close()

@app.get("/admin/fraud-heatmap")
def get_fraud_heatmap():
    """Return hyper-local fraud detection analytics per zone."""
    from app.weather import ZONE_COORDS
    db = SessionLocal()
    try:
        claims = db.query(Claim).all()
        workers = db.query(Worker).all()
        worker_zones = {w.id: w.zone for w in workers}

        zone_stats: dict = {}
        for c in claims:
            zone = worker_zones.get(c.worker_id, "Unknown")
            if zone not in zone_stats:
                coords = ZONE_COORDS.get(zone, (13.0827, 80.2707))
                zone_stats[zone] = {
                    "zone": zone,
                    "lat": coords[0], "lon": coords[1],
                    "total_claims": 0, "auto_approved": 0,
                    "manual_review": 0, "rejected": 0,
                    "avg_fraud_score": 0, "fraud_scores": [],
                }
            z = zone_stats[zone]
            z["total_claims"] += 1
            if c.status == "approved":   z["auto_approved"] += 1
            if c.status == "manual_review": z["manual_review"] += 1
            if c.status == "rejected":   z["rejected"] += 1
            if c.fraud_score is not None:
                z["fraud_scores"].append(c.fraud_score)

        for z in zone_stats.values():
            scores = z.pop("fraud_scores", [])
            z["avg_fraud_score"] = round(sum(scores)/len(scores), 1) if scores else 0
            z["risk_level"] = "HIGH" if z["avg_fraud_score"] > 60 else ("MEDIUM" if z["avg_fraud_score"] > 30 else "LOW")

        return {"zones": list(zone_stats.values()), "total_zones": len(zone_stats)}
    finally:
        db.close()

# Final Static Mount — Handles index.html and all static assets at /
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

import httpx
import asyncio

# Background tasks have been consolidated into app.scheduler

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True, access_log=False, log_level=os.environ.get("UVICORN_LOG_LEVEL", "error").lower())
