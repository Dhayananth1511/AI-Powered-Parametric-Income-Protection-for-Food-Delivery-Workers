"""
Background Job Scheduler — Phase 2A
Handles periodic tasks: disruption monitoring, auto-claims, payment retries.
Framework: APScheduler for scheduling, in-memory state (upgradeable to Redis)
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import logging
from app.database import SessionLocal
from app.models import Claim, DisruptionEvent, Payment, Worker
from app.trigger_monitor import get_zone_status, confirm_disruption, _ZONE_STATE
from app.background_jobs import process_disruptions, expire_disruptions
from app.payment_engine import payment_engine

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = BackgroundScheduler()

# ─────────────────────────────────────────────────────────────────────────────
# Scheduled Tasks
# ─────────────────────────────────────────────────────────────────────────────

def job_check_zone_disruptions():
    """Every 5 minutes: Check weather APIs for disruption triggers."""
    logger.info("🔄 Task: Checking zone disruptions...")
    try:
        from app.weather import get_all_zones
        from app.routes_weather import fetch_weather
        
        zones = get_all_zones()
        disruptions_detected = 0
        
        for zone in zones:
            try:
                weather = fetch_weather(zone)
                if weather and weather.get("has_disruption"):
                    logger.info(f"⚡ Disruption detected in {zone}: {weather.get('alert_type')}")
                    disruptions_detected += 1
            except Exception as e:
                logger.error(f"Error checking zone {zone}: {e}")
        
        logger.info(f"✅ Zone check complete: {disruptions_detected} disruptions detected")
    
    except Exception as e:
        logger.error(f"❌ Error in job_check_zone_disruptions: {e}")

def job_confirm_disruptions():
    """Every 2 minutes: Check confirmation windows and confirm if threshold persistent."""
    logger.info("🔄 Task: Confirming disruptions...")
    try:
        zones_to_check = list(_ZONE_STATE.keys())
        confirmed = 0
        
        for zone in zones_to_check:
            state = _ZONE_STATE.get(zone)
            if state and state.get("status") == "confirming":
                # Check if confirmation window elapsed
                conf_start = state.get("confirmation_start")
                if conf_start:
                    elapsed = (datetime.now() - conf_start).total_seconds() / 60
                    if elapsed >= 20:  # Confirmation window complete
                        logger.info(f"✅ Confirming disruption for {zone}")
                        state["status"] = "confirmed"
                        state["confirmation_end"] = datetime.now()
                        confirmed += 1
        
        logger.info(f"✅ Disruption confirmation check: {confirmed} confirmed")
    
    except Exception as e:
        logger.error(f"❌ Error in job_confirm_disruptions: {e}")

def job_auto_create_claims():
    """When disruption confirmed: Create auto-claims for all zone workers."""
    logger.info("🔄 Task: Creating auto-claims...")
    try:
        process_disruptions()
        logger.info("✅ Auto-claims created")
    
    except Exception as e:
        logger.error(f"❌ Error in job_auto_create_claims: {e}")

def job_expire_disruptions():
    """Every 30 minutes: Expire old confirmed disruptions."""
    logger.info("🔄 Task: Expiring old disruptions...")
    try:
        expire_disruptions()
        logger.info("✅ Old disruptions expired")
    
    except Exception as e:
        logger.error(f"❌ Error in job_expire_disruptions: {e}")

def job_retry_failed_payments():
    """Every 30 minutes: Retry failed payments."""
    logger.info("🔄 Task: Retrying failed payments...")
    db = SessionLocal()
    try:
        failed_payments = db.query(Payment).filter(
            Payment.status == "failed",
            Payment.retry_count < Payment.max_retries
        ).all()
        
        retry_count = 0
        for payment in failed_payments:
            try:
                logger.info(f"🔄 Retrying payment: {payment.id}")
                payment_engine.retry_payment(payment.id)
                retry_count += 1
            except Exception as e:
                logger.error(f"Error retrying payment {payment.id}: {e}")
        
        logger.info(f"✅ Payment retry task: {retry_count} payments retried")
    
    except Exception as e:
        logger.error(f"❌ Error in job_retry_failed_payments: {e}")
    finally:
        db.close()

def job_update_worker_stats():
    """Every hour: Update worker cumulative stats (claims, payouts)."""
    logger.info("🔄 Task: Updating worker stats...")
    db = SessionLocal()
    try:
        workers = db.query(Worker).all()
        updated = 0
        
        for worker in workers:
            try:
                # Count claims and payouts
                claims = db.query(Claim).filter(Claim.worker_id == worker.id).all()
                approved_claims = [c for c in claims if c.status in ["approved", "success"]]
                
                worker.claims_total = len(claims)
                worker.claims_approved = len(approved_claims)
                total_payout = sum(c.payout_amount for c in approved_claims)
                worker.payouts = total_payout
                
                updated += 1
            except Exception as e:
                logger.error(f"Error updating worker {worker.id}: {e}")
        
        db.commit()
        logger.info(f"✅ Worker stats updated: {updated} workers")
    
    except Exception as e:
        logger.error(f"❌ Error in job_update_worker_stats: {e}")
    finally:
        db.close()

def job_cleanup_old_records():
    """Every 24 hours: Clean up old records (older than 90 days)."""
    logger.info("🔄 Task: Cleaning up old records...")
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        
        # Note: Actual cleanup logic depends on retention policy
        # For now, just log
        logger.info(f"✅ Cleanup task: Will remove records older than {cutoff_date}")
    
    except Exception as e:
        logger.error(f"❌ Error in job_cleanup_old_records: {e}")
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Scheduler Initialization
# ─────────────────────────────────────────────────────────────────────────────

def initialize_scheduler():
    """Initialize and start background job scheduler."""
    try:
        # Check zone disruptions every 5 minutes
        scheduler.add_job(
            job_check_zone_disruptions,
            IntervalTrigger(minutes=5),
            id="job_check_zone_disruptions",
            name="Check Zone Disruptions",
            replace_existing=True
        )
        
        # Confirm disruptions every 2 minutes
        scheduler.add_job(
            job_confirm_disruptions,
            IntervalTrigger(minutes=2),
            id="job_confirm_disruptions",
            name="Confirm Disruptions",
            replace_existing=True
        )
        
        # Auto-create claims when disruption confirmed
        scheduler.add_job(
            job_auto_create_claims,
            IntervalTrigger(minutes=1),
            id="job_auto_create_claims",
            name="Auto-Create Claims",
            replace_existing=True
        )
        
        # Expire old disruptions every 30 minutes
        scheduler.add_job(
            job_expire_disruptions,
            IntervalTrigger(minutes=30),
            id="job_expire_disruptions",
            name="Expire Old Disruptions",
            replace_existing=True
        )
        
        # Retry failed payments every 30 minutes
        scheduler.add_job(
            job_retry_failed_payments,
            IntervalTrigger(minutes=30),
            id="job_retry_failed_payments",
            name="Retry Failed Payments",
            replace_existing=True
        )
        
        # Update worker stats every hour
        scheduler.add_job(
            job_update_worker_stats,
            IntervalTrigger(hours=1),
            id="job_update_worker_stats",
            name="Update Worker Stats",
            replace_existing=True
        )
        
        # Cleanup old records at 2 AM daily
        scheduler.add_job(
            job_cleanup_old_records,
            CronTrigger(hour=2, minute=0),
            id="job_cleanup_old_records",
            name="Cleanup Old Records",
            replace_existing=True
        )
        
        if not scheduler.running:
            scheduler.start()
            logger.info("✅ Background scheduler started")
        else:
            logger.info("ℹ️  Scheduler already running")
    
    except Exception as e:
        logger.error(f"❌ Error initializing scheduler: {e}")

def stop_scheduler():
    """Stop background job scheduler."""
    try:
        if scheduler.running:
            scheduler.shutdown()
            logger.info("✅ Scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")

def get_scheduler_status():
    """Get scheduler status and list of jobs."""
    return {
        "running": scheduler.running,
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "trigger": str(job.trigger),
                "next_run_time": str(job.next_run_time) if job.next_run_time else None
            }
            for job in scheduler.get_jobs()
        ]
    }
