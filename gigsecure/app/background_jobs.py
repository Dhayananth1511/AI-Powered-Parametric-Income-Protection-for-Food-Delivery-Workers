"""
Background Job System — Autonomous Disruption Monitoring & Auto-Claim Triggering
Real-time 15-second polling for claims automation
"""
import logging
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from typing import Dict, List, Optional
from app.database import SessionLocal
from app.models import Worker, Claim, DisruptionEvent
from app.trigger_monitor import get_zone_status, simulate_disruption, get_active_events
from app.claims import run_claim_pipeline, calculate_payout
import uuid
import json

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Global Scheduler Instance
# ─────────────────────────────────────────────────────────────────────────────
scheduler: Optional[BackgroundScheduler] = None

# ─────────────────────────────────────────────────────────────────────────────
# Scheduler Lifecycle
# ─────────────────────────────────────────────────────────────────────────────
def start_scheduler():
    """Initialize and start background scheduler."""
    global scheduler
    
    if scheduler and scheduler.running:
        logger.info("Scheduler already running")
        return
    
    scheduler = BackgroundScheduler(daemon=True)
    
    # Job 1: Monitor disruptions and auto-trigger claims (15 seconds)
    scheduler.add_job(
        func=_auto_trigger_claims,
        trigger=IntervalTrigger(seconds=15),
        id="auto_trigger_claims",
        name="Auto-Trigger Claims on Disruption",
        replace_existing=True,
    )
    
    # Job 2: Weekly reset of hourly limits (every Sunday at 00:00 UTC)
    scheduler.add_job(
        func=_weekly_reset,
        trigger="cron",
        day_of_week="6",
        hour="0",
        minute="0",
        id="weekly_reset",
        name="Weekly Reset — Hourly Limits",
        replace_existing=True,
    )
    
    # Job 3: Plan expiry notifications (every hour)
    scheduler.add_job(
        func=_check_plan_expiry,
        trigger=IntervalTrigger(hours=1),
        id="check_plan_expiry",
        name="Check Plan Expiry & Send Notifications",
        replace_existing=True,
    )
    
    # Job 4: Clean up old disruption events (daily)
    scheduler.add_job(
        func=_cleanup_old_events,
        trigger=IntervalTrigger(hours=24),
        id="cleanup_old_events",
        name="Clean Up Old Disruption Events",
        replace_existing=True,
    )
    
    scheduler.start()
    logger.info("✅ Background Scheduler Started — 4 jobs registered")

def stop_scheduler():
    """Stop background scheduler."""
    global scheduler
    
    if scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("✅ Scheduler stopped")

def get_scheduler_status() -> dict:
    """Get current scheduler status."""
    if not scheduler:
        return {"status": "not_initialized", "jobs": []}
    
    jobs_info = []
    for job in scheduler.get_jobs():
        jobs_info.append({
            "id": job.id,
            "name": job.name,
            "next_run": str(job.next_run_time) if job.next_run_time else "N/A",
            "trigger": str(job.trigger),
        })
    
    return {
        "status": "running" if scheduler.running else "stopped",
        "jobs_count": len(jobs_info),
        "jobs": jobs_info,
    }

# ─────────────────────────────────────────────────────────────────────────────
# Job 1: Auto-Trigger Claims
# ─────────────────────────────────────────────────────────────────────────────
def _auto_trigger_claims():
    """
    Monitor active disruption events and auto-trigger claims for affected workers.
    Runs every 15 seconds.
    """
    try:
        db = SessionLocal()
        
        # Get all active disruptions
        active_disruptions = get_active_events()
        
        if not active_disruptions:
            return
        
        logger.info(f"🌩️  Auto-trigger check: Found {len(active_disruptions)} active disruptions")
        
        for disruption_id, disruption in active_disruptions.items():
            zone = disruption.get("zone", "")
            trigger = disruption.get("trigger", {})
            event_start = disruption.get("confirmation_end")
            
            if not event_start:
                continue
            
            # Calculate disruption duration
            disruption_hrs = (datetime.now() - event_start).total_seconds() / 3600
            
            # Find all workers in this zone with active plans
            workers = db.query(Worker).filter(
                Worker.zone == zone,
                Worker.is_active == True,
                Worker.plan != None,
            ).all()
            
            for worker in workers:
                # Skip if worker already has claim for this disruption
                existing_claim = db.query(Claim).filter(
                    Claim.worker_id == worker.id,
                    Claim.trigger_type == trigger.get("type"),
                    Claim.created_at > (datetime.now() - timedelta(hours=disruption_hrs + 1)),
                ).first()
                
                if existing_claim:
                    continue
                
                # Auto-trigger claim
                try:
                    worker_dict = {
                        "id": worker.id,
                        "name": worker.name,
                        "zone": worker.zone,
                        "plan": worker.plan,
                        "trust_score": worker.trust_score or 40,
                        "claims_total": worker.claims_total or 0,
                    }
                    
                    result = run_claim_pipeline(worker_dict, trigger, disruption_hrs)
                    
                    # Create claim record
                    claim = Claim(
                        id="CLM-" + uuid.uuid4().hex[:6].upper(),
                        worker_id=worker.id,
                        trigger_type=trigger.get("type", ""),
                        trigger_value=float(trigger.get("value", 0)),
                        trigger_label=trigger.get("label", "Alert"),
                        disruption_hrs=disruption_hrs,
                        payout_amount=result.get("payout", 0),
                        fraud_score=result.get("fraud", {}).get("fraud_score", 0),
                        status=result.get("status", "pending"),
                        notes=result.get("fraud", {}).get("decision", ""),
                        pipeline_steps=json.dumps(result.get("steps", [])),
                        is_simulated=False,  # This is REAL auto-trigger
                    )
                    db.add(claim)
                    
                    # Update worker stats
                    if result.get("status") in ["approved", "manual_review"]:
                        worker.claims_approved = (worker.claims_approved or 0) + 1
                        worker.payouts = (worker.payouts or 0) + result.get("payout", 0)
                        worker.earnings_protected = (worker.earnings_protected or 0) + result.get("payout", 0)
                    
                    db.commit()
                    logger.info(f"✅ Auto-claim triggered: {worker.id} | {worker.name} | ₹{result.get('payout', 0)}")
                    
                except Exception as e:
                    logger.error(f"❌ Error auto-triggering claim for {worker.id}: {e}")
                    db.rollback()
        
        db.close()
    
    except Exception as e:
        logger.error(f"❌ Auto-trigger job failed: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Job 2: Weekly Reset
# ─────────────────────────────────────────────────────────────────────────────
def _weekly_reset():
    """
    Reset weekly hourly limits for all workers every Sunday.
    """
    try:
        db = SessionLocal()
        
        workers = db.query(Worker).all()
        reset_count = 0
        
        for worker in workers:
            worker.weekly_hrs_used = 0.0
            worker.weekly_reset_at = datetime.now()
            reset_count += 1
        
        db.commit()
        db.close()
        
        logger.info(f"✅ Weekly reset completed: {reset_count} workers")
    
    except Exception as e:
        logger.error(f"❌ Weekly reset job failed: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Job 3: Plan Expiry Check
# ─────────────────────────────────────────────────────────────────────────────
def _check_plan_expiry():
    """
    Check for expiring plans and send notifications.
    """
    try:
        db = SessionLocal()
        
        # Find plans expiring in next 3 days
        expiry_threshold = datetime.now() + timedelta(days=3)
        
        workers = db.query(Worker).filter(
            Worker.plan_effective_date != None,
            Worker.plan_expiry_notified == False,
        ).all()
        
        notif_count = 0
        for worker in workers:
            expiry_date = worker.plan_effective_date + timedelta(days=30)
            
            if datetime.now() < expiry_date < expiry_threshold:
                days_left = (expiry_date - datetime.now()).days
                logger.info(f"⏰ Plan expiring in {days_left} days: {worker.id} | {worker.name}")
                
                worker.plan_expiry_notified = True
                notif_count += 1
        
        db.commit()
        db.close()
        
        if notif_count > 0:
            logger.info(f"✅ Expiry notifications sent: {notif_count} workers")
    
    except Exception as e:
        logger.error(f"❌ Plan expiry check job failed: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Job 4: Cleanup Old Events
# ─────────────────────────────────────────────────────────────────────────────
def _cleanup_old_events():
    """
    Delete disruption events older than 7 days.
    """
    try:
        db = SessionLocal()
        
        cutoff_date = datetime.now() - timedelta(days=7)
        
        deleted = db.query(DisruptionEvent).filter(
            DisruptionEvent.created_at < cutoff_date
        ).delete()
        
        db.commit()
        db.close()
        
        logger.info(f"✅ Cleanup completed: Deleted {deleted} old disruption events")
    
    except Exception as e:
        logger.error(f"❌ Cleanup job failed: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Utility: Get job history/execution logs
# ─────────────────────────────────────────────────────────────────────────────
def get_job_logs() -> List[dict]:
    """Get recent job execution logs."""
    if not scheduler:
        return []
    
    logs = []
    for job in scheduler.get_jobs():
        logs.append({
            "job_id": job.id,
            "job_name": job.name,
            "next_run": str(job.next_run_time),
            "trigger": str(job.trigger),
            "last_run": job.next_run_time - timedelta(seconds=60) if job.next_run_time else None,
        })
    
    return logs
def process_disruptions():
    """
    Process confirmed disruptions and create claims for affected workers.
    This reuses the existing auto-trigger job logic.
    """
    _auto_trigger_claims()


def expire_disruptions():
    """
    Clear in-memory confirmed disruptions that have been active too long.
    Also marks old DB disruption events as cleared.
    """
    db = SessionLocal()
    try:
        now = datetime.now()
        expired_zones = []

        for zone, state in list(get_active_events().items()) if isinstance(get_active_events(), dict) else []:
            confirmation_end = state.get("confirmation_end")
            if confirmation_end and (now - confirmation_end) > timedelta(hours=6):
                expired_zones.append(zone)

        for zone in expired_zones:
            from app.trigger_monitor import clear_disruption
            clear_disruption(zone)

        old_events = db.query(DisruptionEvent).filter(
            DisruptionEvent.status == "confirmed",
            DisruptionEvent.created_at < (now - timedelta(hours=6))
        ).all()

        for event in old_events:
            event.status = "cleared"

        db.commit()
        logger.info(f"✅ Expired disruptions cleared: {len(expired_zones)} zones, {len(old_events)} DB events")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ expire_disruptions failed: {e}")
    finally:
        db.close()
