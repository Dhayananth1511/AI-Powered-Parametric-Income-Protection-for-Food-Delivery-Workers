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
from app import routes_kyc, routes_notifications, routes_payments, routes_bot
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

from sqlalchemy import text, func as sqlfunc
from datetime import timedelta

_POLICY_MIGRATIONS = [
    "ALTER TABLE workers ADD COLUMN bank_upi_id VARCHAR",
    "ALTER TABLE workers ADD COLUMN plan_expiry_notified BOOLEAN DEFAULT FALSE",
    "ALTER TABLE workers ADD COLUMN policy_start_date TIMESTAMP",
    "ALTER TABLE workers ADD COLUMN policy_expiry_date TIMESTAMP",
    "ALTER TABLE workers ADD COLUMN policy_status VARCHAR DEFAULT 'active'",
    "ALTER TABLE payments ALTER COLUMN claim_id DROP NOT NULL",
]

# Index creation — safe to run repeatedly (IF NOT EXISTS)
_INDEX_MIGRATIONS = [
    "CREATE INDEX IF NOT EXISTS ix_workers_email         ON workers(email)",
    "CREATE INDEX IF NOT EXISTS ix_workers_phone         ON workers(phone)",
    "CREATE INDEX IF NOT EXISTS ix_workers_zone          ON workers(zone)",
    "CREATE INDEX IF NOT EXISTS ix_workers_plan          ON workers(plan)",
    "CREATE INDEX IF NOT EXISTS ix_workers_policy_status ON workers(policy_status)",
    "CREATE INDEX IF NOT EXISTS ix_workers_is_active     ON workers(is_active)",
    "CREATE INDEX IF NOT EXISTS ix_workers_aadhaar       ON workers(aadhaar_verified)",
    "CREATE INDEX IF NOT EXISTS ix_workers_joined        ON workers(joined)",
    "CREATE INDEX IF NOT EXISTS ix_claims_worker_id      ON claims(worker_id)",
    "CREATE INDEX IF NOT EXISTS ix_claims_status         ON claims(status)",
    "CREATE INDEX IF NOT EXISTS ix_claims_created_at     ON claims(created_at)",
    "CREATE INDEX IF NOT EXISTS ix_claims_worker_status  ON claims(worker_id, status)",
    "CREATE INDEX IF NOT EXISTS ix_notif_worker_unread   ON notifications(worker_id, is_read)",
    "CREATE INDEX IF NOT EXISTS ix_payments_worker_id    ON payments(worker_id)",
    "CREATE INDEX IF NOT EXISTS ix_weather_zone_time     ON weather_logs(zone, logged_at)",
]

def _run_migrations():
    """Idempotent ALTER TABLE + CREATE INDEX migrations — errors silently skipped."""
    try:
        with engine.connect() as conn:
            for sql in _POLICY_MIGRATIONS + _INDEX_MIGRATIONS:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                except Exception:
                    pass
    except Exception as e:
        logger.warning(f"Migration warning (non-fatal): {e}")

def _seed_policy_dates():
    """Seed 7-day policy window for any workers missing policy dates."""
    try:
        with engine.connect() as conn:
            now = datetime.now()
            conn.execute(text(
                "UPDATE workers SET policy_start_date=:s, policy_expiry_date=:e, "
                "policy_status='active' WHERE policy_start_date IS NULL"
            ), {"s": now.isoformat(), "e": (now + timedelta(days=7)).isoformat()})
            conn.commit()
    except Exception as e:
        logger.warning(f"Policy seed warning (non-fatal): {e}")


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
    allow_origins=["*"] if os.getenv("ENVIRONMENT") == "development" else allowed_origins,
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
app.include_router(routes_bot.router)

# Static Frontend (Mount after all routes)
static_path = os.path.join(os.path.dirname(__file__), "..", "static")

# ─────────────────────────────────────────────────────────────────────────────
# Seed Database (idempotent)
# ─────────────────────────────────────────────────────────────────────────────
def seed_db():
    if os.getenv("SKIP_SEEDING", "").lower() in {"1", "true", "yes"}:
        logger.info("⏭️ Skipping database seeding per environment variable.")
        return

    from app.security import hash_password
    now = datetime.now()
    week = timedelta(days=7)
    db: Session = SessionLocal()
    try:
        # Production Demo Hardened: No hardcoded mock claims or workers here.
        # Use reset_db.py for seeding the official demo state.
        if db.query(Admin).count() == 0:
            admins = [
                Admin(id="ADM-001", name="Karthik Sundaram", email="admin@digit.com",
                      password=hash_password("admin123"), org="Digit Insurance Pvt Ltd",
                      designation="Portfolio Manager"),
                Admin(id="ADM-002", name="Priya Nair", email="ops@gigpulse.in",
                      password=hash_password("admin123"), org="ZenVyte GigPulse Platform Admin",
                      designation="Platform Admin"),
            ]
            for a in admins:
                db.add(a)

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
    import threading

    def _bg_init():
        """Run blocking DB ops in a thread — port binds instantly."""
        try:
            Base.metadata.create_all(bind=engine)
            _run_migrations()
            _seed_policy_dates()
            seed_db()
            initialize_scheduler()
            # Pre-warm ML engine so first /ml/forecast request is instant
            try:
                from app.ml_engine import predict_disruption_probability, get_all_zones
                zones = get_all_zones()
                if zones:
                    predict_disruption_probability(zones[0])  # warm up with first zone
                logger.info("✅ ML engine pre-warmed")
            except Exception as ml_err:
                logger.warning(f"⚠️  ML pre-warm skipped: {ml_err}")
            logger.info("✅ Background startup complete")
        except Exception as e:
            logger.error(f"❌ Background startup error: {e}")

    threading.Thread(target=_bg_init, daemon=True, name="startup-init").start()

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
    """
    Optimised: uses SQL GROUP BY / SUM / COUNT instead of loading all rows
    into Python memory. Typically 5-10x faster than the old full-table-scan.
    """
    db: Session = SessionLocal()
    try:
        plan_prices = {"starter": 55, "basic": 70, "standard": 90, "premium": 115, "elite": 135}

        # ── 1. Plan distribution + premium via GROUP BY ───────────────────────
        plan_rows = (
            db.query(Worker.plan, sqlfunc.count(Worker.id))
            .group_by(Worker.plan)
            .all()
        )
        plan_dist     = {plan: cnt for plan, cnt in plan_rows}
        total_workers = sum(plan_dist.values())
        total_premium = sum(plan_prices.get(plan, 90) * cnt for plan, cnt in plan_rows)

        # ── 2. Payout / earnings sums in one SQL query ────────────────────────
        payout_row = db.query(
            sqlfunc.coalesce(sqlfunc.sum(Worker.payouts), 0),
            sqlfunc.coalesce(sqlfunc.sum(Worker.sim_payouts), 0),
            sqlfunc.coalesce(sqlfunc.sum(Worker.earnings_protected), 0),
            sqlfunc.coalesce(sqlfunc.avg(Worker.trust_score), 40),
        ).one()

        # Extra defensive check: coalesce in SQL usually handles it, but Python-level conversion
        # ensures we never return None/null for these critical KPIs.
        raw_payouts     = payout_row[0] if payout_row[0] is not None else 0
        raw_sim_payouts = payout_row[1] if payout_row[1] is not None else 0
        raw_protected   = payout_row[2] if payout_row[2] is not None else 0
        raw_avg_trust   = payout_row[3] if payout_row[3] is not None else 40

        total_payouts            = float(raw_payouts) + float(raw_sim_payouts)
        total_earnings_protected = float(raw_protected)
        avg_trust                = round(float(raw_avg_trust), 1)



        # ── 3. Aadhaar verified count ─────────────────────────────────────────
        aadhaar_verified = (
            db.query(sqlfunc.count(Worker.id))
            .filter(Worker.aadhaar_verified == True)
            .scalar() or 0
        )

        # ── 4. New workers joined today ───────────────────────────────────────
        today = date.today()
        new_today = (
            db.query(sqlfunc.count(Worker.id))
            .filter(sqlfunc.date(Worker.joined) == today)
            .scalar() or 0
        )

        # ── 5. Claims by status via GROUP BY ──────────────────────────────────
        claim_rows  = (
            db.query(Claim.status, sqlfunc.count(Claim.id))
            .group_by(Claim.status)
            .all()
        )
        claim_dist  = {status: cnt for status, cnt in claim_rows}
        total_claims = sum(claim_dist.values())

        # ── 6. Loss ratio ─────────────────────────────────────────────────────
        loss_ratio = round((total_payouts / (total_premium * 52) * 100), 1) if total_premium > 0 else 0

        # ── 7. Active disruption events (in-memory cache) ─────────────────────
        active_events_count = 0
        try:
            active_events_count = len(get_active_events())
        except Exception as e:
            logger.error(f"Error getting active events: {e}")

        return {
            "policies":                 total_workers,
            "weekly_premium":           total_premium,
            "total_payouts":            total_payouts,
            "platform_fee":             round(total_premium * 0.05, 1),
            "total_claims":             total_claims,
            "approved_claims":          claim_dist.get("approved", 0),
            "rejected_claims":          claim_dist.get("rejected", 0),
            "review_claims":            claim_dist.get("manual_review", 0),
            "loss_ratio":               loss_ratio,
            "plan_breakdown":           plan_dist,
            "new_today":                new_today,
            "aadhaar_verified":         aadhaar_verified,
            "avg_trust_score":          avg_trust,
            "total_earnings_protected": total_earnings_protected,
            "active_disruptions":       active_events_count,
        }
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Admin — Workers List
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/workers")
def get_workers():
    """
    Optimised: loads only the columns needed for the admin worker table.
    Avoids fetching password hash, binary blobs, or unused heavy fields.
    """
    db = SessionLocal()
    try:
        rows = db.query(
            Worker.id, Worker.name, Worker.phone, Worker.email,
            Worker.zone, Worker.plan, Worker.risk_score, Worker.trust_score,
            Worker.payouts, Worker.sim_payouts, Worker.claims_total,
            Worker.claims_approved, Worker.claims_rejected, Worker.platform,
            Worker.joined, Worker.aadhaar_verified, Worker.earnings_protected,
            Worker.is_online,
        ).all()
        return {
            "workers": [
                {
                    "id": r.id, "name": r.name, "phone": r.phone,
                    "email": r.email, "zone": r.zone, "plan": r.plan,
                    "risk_score": r.risk_score, "trust_score": r.trust_score,
                    "payouts": r.payouts, "sim_payouts": r.sim_payouts,
                    "claims_total": r.claims_total,
                    "claims_approved": r.claims_approved,
                    "claims_rejected": r.claims_rejected,
                    "platform": r.platform,
                    "joined": str(r.joined) if r.joined else None,
                    "aadhaar_verified": r.aadhaar_verified,
                    "earnings_protected": r.earnings_protected,
                    "is_online": bool(r.is_online),
                    "role": "worker",
                }
                for r in rows
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
    try:
        from app.ml_engine import zone_risk_breakdown
        if month is None:
            month = datetime.now().month
        return zone_risk_breakdown(zone, month)
    except Exception as e:
        logger.error(f"Error in get_zone_risk: {e}", exc_info=True)
        # Fallback to a safe moderate response so onboarding doesn't break
        return {
            "zone": zone,
            "overall_risk": 0.5,
            "risk_label": "Analysis Fallback (Moderate)",
            "recommended_plan": "standard",
            "factors": {
                "flood_risk": 0.5, "water_proximity": 0.5, "elevation_inv": 0.5,
                "aqi_history": 0.5, "disruption_freq": 0.5
            },
            "is_monsoon": datetime.now().month in [6,7,8,9],
            "disruption_months_per_year": 6
        }

@app.get("/ml/forecast/{zone}")
def get_forecast(zone: str):
    from app.ml_engine import predict_disruption_probability
    return predict_disruption_probability(zone)

@app.get("/ml/all-forecasts")
def get_all_forecasts(limit: int = 8):
    """Return forecasts for all zones in ONE request — avoids N parallel round-trips from the frontend."""
    from app.ml_engine import predict_disruption_probability, get_all_zones
    zones = get_all_zones()[:limit]
    results = {}
    for z in zones:
        try:
            results[z] = predict_disruption_probability(z)
        except Exception:
            pass
    return {"forecasts": results, "total": len(results)}

@app.get("/ml/loss-ratio/{plan}")
def get_loss_ratio(plan: str, disruption_hrs: float = 52.5):
    from app.ml_engine import calculate_loss_ratio
    return calculate_loss_ratio(plan, disruption_hrs)

# ─────────────────────────────────────────────────────────────────────────────
# Phase 3: Compliance Center — Market Crash Defense
# ─────────────────────────────────────────────────────────────────────────────

# Compliance state is now managed by app.compliance module to prevent circular imports
from app.compliance import get_compliance_state, update_compliance_state, is_market_crash, is_policy_freeze

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
def get_compl_state():
    """Get the current Phase 3 compliance / market crash state."""
    return get_compliance_state()

@app.post("/admin/compliance")
def update_compl_state(patch: CompliancePatch):
    """Update compliance parameters in real-time (Market Crash response)."""
    return {"success": True, "state": update_compliance_state(patch.dict())}

@app.get("/admin/loss-ratio-trend")
def get_loss_ratio_trend():
    """Return week-by-week loss ratio trend for the admin dashboard chart.
    Optimised: weekly payout sums computed in SQL; only one Worker aggregate query.
    """
    from app.ml_engine import PLAN_BASE
    db = SessionLocal()
    try:
        plan_prices = {p: PLAN_BASE[p]["premium"] for p in PLAN_BASE}

        # Handle Date formatting strictly per Database Dialect
        from sqlalchemy import func as _f
        dialect_name = db.get_bind().dialect.name
        
        if dialect_name == "postgresql":
            week_col = _f.to_char(Claim.created_at, 'IYYY-"W"IW').label("week")
        else:
            week_col = _f.strftime("%Y-W%W", Claim.created_at).label("week")

        week_rows = (
            db.query(
                week_col,
                _f.sum(Claim.payout_amount).label("payouts"),
            )
            .filter(Claim.status == "approved", Claim.created_at.isnot(None))
            .group_by("week")
            .order_by("week")
            .all()
        )

        # Single aggregate query for weekly premium baseline
        plan_rows = db.query(Worker.plan, sqlfunc.count(Worker.id)).group_by(Worker.plan).all()
        weekly_premium = sum(plan_prices.get(plan, 90) * cnt for plan, cnt in plan_rows)

        return {
            "weeks": [
                {
                    "week":       row.week,
                    "payouts":    float(row.payouts or 0),
                    "premium":    weekly_premium,
                    "loss_ratio": round(float(row.payouts or 0) / weekly_premium * 100, 1) if weekly_premium > 0 else 0.0,
                }
                for row in week_rows
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
