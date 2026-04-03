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
from app.database import engine, Base, SessionLocal
from app.models import Worker, Admin, Policy, Claim, WeatherLog
from app import routes_auth, routes_policy, routes_claims, routes_weather
from app import routes_kyc, routes_notifications, routes_payments
from app.ml_engine import compute_risk_score, recommend_plan, calculate_dynamic_premium
from app.trigger_monitor import get_active_events, get_all_disruption_events_db
from app.background_jobs import start_scheduler, stop_scheduler, get_scheduler_status
from app.scheduler import initialize_scheduler, stop_scheduler as stop_bg_scheduler
from sqlalchemy.orm import Session
from datetime import datetime, date
import os
import logging

# ─────────────────────────────────────────────────────────────────────────────
# Configure Logging
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("gigsecure.log", encoding='utf-8'),
    ]
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Create all tables
# ─────────────────────────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

from sqlalchemy import text
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE workers ADD COLUMN bank_upi_id VARCHAR"))
        conn.commit()
    except Exception:
        pass
    try:
        conn.execute(text("ALTER TABLE workers ADD COLUMN plan_expiry_notified BOOLEAN DEFAULT 0"))
        conn.commit()
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="GigSecure API",
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
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

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
                    email="ops@gigsecure.in", password=hash_password("admin123"),
                    org="GigSecure Platform Admin", designation="Platform Admin",
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

seed_db()

# ─────────────────────────────────────────────────────────────────────────────
# Startup & Shutdown Events (Lifecycle Management)
# ─────────────────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Start background jobs on application startup."""
    logger.info("🚀 GigSecure API Starting...")
    print("━" * 70)
    print("🛡️  GigSecure — AI-Powered Parametric Income Protection")
    print("━" * 70)
    start_scheduler()
    initialize_scheduler()  # Phase 2A: Initialize new scheduler
    logger.info("✅ Startup complete — Background jobs active")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop background jobs on application shutdown."""
    logger.info("⛔ GigSecure API Shutting Down...")
    stop_scheduler()
    stop_bg_scheduler()  # Phase 2A: Stop new scheduler
    logger.info("✅ Shutdown complete")

# ─────────────────────────────────────────────────────────────────────────────
# Root & Health
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api")
def api_root():
    return {
        "app":     "GigSecure API v2.0",
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
@app.get("/admin/stats")
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
# ML — Zone Info
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

# Final Static Mount — Handles index.html and all static assets at /
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

import httpx
import asyncio

async def weather_poller():
    """15-second background poller for realtime parametric monitoring"""
    while True:
        await asyncio.sleep(15)
        try:
            from app.weather import fetch_weather, check_triggers
            from app.trigger_monitor import get_zone_status
            from app.database import SessionLocal
            from app.models import Worker
            
            # 1. Find which zones currently have active workers
            db = SessionLocal()
            try:
                active_zones = {w.zone for w in db.query(Worker).filter(Worker.is_active == True).all()}
            finally:
                db.close()

            # 2. Poll those zones
            for zone in active_zones:
                weather = await fetch_weather(zone)
                triggers = check_triggers(weather)
                
                # 3. Auto-Trigger Pipeline if weather hits threshold!
                if triggers:
                    status = get_zone_status(zone)
                    if not status.get("payout_active"):
                        # Hit the auto-pipeline endpoint locally to trigger zero-touch payout
                        async with httpx.AsyncClient() as client:
                            await client.post(
                                "http://127.0.0.1:8000/claims/zone-simulate",
                                json={"zone": zone, "trigger_type": triggers[0]["type"]}
                            )
        except Exception as e:
            print(f"[Background Poller Error] {e}")

async def subscription_poller():
    """Checks for expired weekly plans and sends renewal prompts securely"""
    while True:
        await asyncio.sleep(60) # Run every 60 seconds
        try:
            from app.database import SessionLocal
            from app.models import Worker, NotificationLog
            from datetime import datetime
            
            db = SessionLocal()
            try:
                # Find workers whose plan expired, but we haven't notified yet
                now = datetime.now()
                expired_workers = db.query(Worker).filter(
                    Worker.weekly_reset_at < now,
                    Worker.plan_expiry_notified == False
                ).all()
                
                for w in expired_workers:
                    # Log internal push notification
                    notif = NotificationLog(
                        worker_id  = w.id,
                        title      = "⚠️ Weekly Plan Expired!",
                        message    = f"Your {w.plan.capitalize()} plan has expired. Please renew ASAP to stay protected against disruptions.",
                        notif_type = "plan_change",
                        icon       = "⏳",
                    )
                    # Set notified flag so we don't spam
                    w.plan_expiry_notified = True
                    db.add(notif)
                    
                    # Log a "Real Message" output simulation
                    msg = (f"[REAL SMS SIMULATION - TWILIO/VONAGE]\n"
                           f"To: {w.phone} | Worker: {w.name}\n"
                           f"Body: 'GigSecure Alert: Your {w.plan.capitalize()} protection plan expired. "
                           f"Open GigSecure app to renew matching your bank ID {w.bank_upi_id or 'Not Pinned'}.'")
                    print("-" * 50)
                    print(msg)
                    print("-" * 50)
                    
                db.commit()
            finally:
                db.close()
        except Exception as e:
            print(f"[Subscription Engine Error] {e}")

@app.on_event("startup")
async def startup_event():
    import asyncio
    asyncio.create_task(weather_poller())
    asyncio.create_task(subscription_poller())

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print("Starting GigSecure Unified Service...")
    print(f"Access the app at: http://localhost:{port}")
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
