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
from app.models import Claim, DisruptionEvent, Payment, Worker, NotificationLog
from app.trigger_monitor import get_zone_status, confirm_disruption, _ZONE_STATE, get_active_events, CONFIRMATION_MINUTES
from app.payment_engine import payment_engine
import uuid
import json

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = BackgroundScheduler()

# ─────────────────────────────────────────────────────────────────────────────
# Scheduled Tasks
# ─────────────────────────────────────────────────────────────────────────────

async def check_all_zones_concurrently():
    """Fetch weather for all zones and feed trigger data into trigger_monitor."""
    from app.weather import get_all_zones, fetch_weather, check_triggers
    from app.trigger_monitor import start_confirmation_window, get_zone_status, _ZONE_STATE
    import asyncio

    zones = get_all_zones()
    # Limit to a batch to avoid hammering the API on free tiers
    batch = zones[:20]
    
    from app.ml_engine import latest_telemetry
    
    tasks = []
    for zone in batch:
        lat, lon = None, None
        for t_data in latest_telemetry.values():
            if t_data.get("zone") == zone and "lat" in t_data:
                lat, lon = t_data["lat"], t_data["lon"]
                break
        tasks.append(fetch_weather(zone, lat, lon))
        
    results = await asyncio.gather(*tasks, return_exceptions=True)

    disruptions_detected = 0
    for i, weather in enumerate(results):
        zone = batch[i]
        if isinstance(weather, Exception):
            logger.warning(f"Weather fetch failed for {zone}: {weather}")
            continue

        triggers = check_triggers(weather)
        if not triggers:
            continue

        trigger = triggers[0]  # Use the most critical trigger
        current_state = _ZONE_STATE.get(zone, {})

        # Only start a new confirmation if not already tracking this zone
        if current_state.get("status") not in ("confirming", "confirmed"):
            logger.info(f"⚡ Trigger detected in {zone}: {trigger['label']} ({trigger['value']}{trigger['unit']})")
            start_confirmation_window(zone, trigger)
            disruptions_detected += 1

    return disruptions_detected

def job_check_zone_disruptions():
    """Every 15 minutes: Check weather APIs for disruption triggers."""
    logger.info("🔄 Task: Checking zone disruptions...")
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            disruptions_detected = loop.run_until_complete(check_all_zones_concurrently())
            logger.info(f"✅ Zone check complete: {disruptions_detected} disruptions detected")
        finally:
            loop.close()
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
                    if elapsed >= CONFIRMATION_MINUTES:  # Confirmation window complete
                        logger.info(f"✅ Confirming disruption for {zone}")
                        confirm_disruption(zone)
                        confirmed += 1
        
        logger.info(f"✅ Disruption confirmation check: {confirmed} confirmed")
    
    except Exception as e:
        logger.error(f"❌ Error in job_confirm_disruptions: {e}")

def job_auto_create_claims():
    """Check for active disruptions and trigger claims logic."""
    logger.info("🔄 Task: Creating auto-claims...")
    db = SessionLocal()
    try:
        from app.claims import run_claim_pipeline
        active_disruptions = [d for d in get_active_events() if d["status"] == "confirmed"]
        
        if not active_disruptions:
            return
            
        logger.info(f"🌩️  Auto-trigger check: Found {len(active_disruptions)} active disruptions")
        
        for disruption in active_disruptions:
            zone = disruption.get("zone", "")
            trigger = disruption.get("trigger", {})
            
            # Logic from legacy background_jobs.py consolidated here
            workers = db.query(Worker).filter(
                Worker.zone == zone,
                Worker.is_active == True,
                Worker.policy_status == "active"
            ).all()
            
            for worker in workers:
                try:
                    # Basic auto-trigger for demo (payout based on plan)
                    worker_dict = {
                        "id": worker.id, "name": worker.name, "zone": worker.zone, 
                        "plan": worker.plan, "weekly_hrs_used": float(worker.weekly_hrs_used or 0.0)
                    }
                    result = run_claim_pipeline(worker_dict, trigger, 4.0, worker_dict["weekly_hrs_used"]) 
                    
                    # Force IST timestamp
                    from datetime import datetime
                    created_at = datetime.fromisoformat(result["timestamp_ist"]) if "timestamp_ist" in result else datetime.utcnow()
                    
                    claim = Claim(
                        id="CLM-" + uuid.uuid4().hex[:6].upper(),
                        worker_id=worker.id,
                        trigger_type=trigger.get("type", "rainfall"),
                        trigger_value=float(trigger.get("value", 0)),
                        trigger_label=trigger.get("label", "Alert"),
                        disruption_hrs=4.0,
                        payout_amount=result.get("payout", 0),
                        status="approved",
                        is_simulated=False,
                        created_at=created_at
                    )
                    db.add(claim)
                    # Update worker stats
                    worker.weekly_hrs_used = (worker.weekly_hrs_used or 0) + result.get("hrs_added", 0)
                    worker.payouts = (worker.payouts or 0) + result.get("payout", 0)
                    worker.earnings_protected = (worker.earnings_protected or 0) + result.get("payout", 0)

                    logger.info(f"✅ Auto-claim triggered: {worker.id} | ₹{result.get('payout', 0)}")
                except Exception as e:
                    logger.error(f"Error auto-triggering claim for {worker.id}: {e}")
        
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error in job_auto_create_claims: {e}")
    finally:
        db.close()

def job_expire_disruptions():
    """Clear old confirmed disruptions from state and DB."""
    logger.info("🔄 Task: Expiring old disruptions...")
    db = SessionLocal()
    try:
        from app.trigger_monitor import clear_disruption
        now = datetime.now()
        
        # Expire in-memory zones
        for zone, state in list(_ZONE_STATE.items()):
            if state["status"] == "confirmed":
                conf_end = state.get("confirmation_end")
                if conf_end and (now - conf_end) > timedelta(hours=6):
                    clear_disruption(zone)
                    logger.info(f"⌛ Expired zone disruption: {zone}")
        
        # Mark DB events as cleared
        old_events = db.query(DisruptionEvent).filter(
            DisruptionEvent.status == "confirmed",
            DisruptionEvent.created_at < (now - timedelta(hours=6))
        ).all()
        for evt in old_events:
            evt.status = "cleared"
        
        db.commit()
        logger.info("✅ Expiration task complete")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error in job_expire_disruptions: {e}")
    finally:
        db.close()

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
# Policy Lifecycle Auto-Check (Daily)
# ─────────────────────────────────────────────────────────────────────────────

def job_policy_lifecycle():
    """Daily job: auto-expire policies, send 24hr warning notifications."""
    logger.info("🔄 Task: Policy lifecycle check...")
    db = SessionLocal()
    try:
        import uuid as _uuid
        from datetime import timedelta
        now = datetime.now()
        workers = db.query(Worker).all()
        expired_count = 0
        alerted_count = 0

        for w in workers:
            if not w.policy_expiry_date:
                # Set a default 7-day window if missing
                w.policy_start_date = now
                w.policy_expiry_date = now + timedelta(days=7)
                w.policy_status = "active"
                continue

            days_left = (w.policy_expiry_date - now).days
            hours_left = (w.policy_expiry_date - now).total_seconds() / 3600

            if now > w.policy_expiry_date:
                # ── EXPIRED: suspend coverage
                if w.policy_status != "expired":
                    w.policy_status = "expired"
                    w.is_active = False
                    expired_count += 1
                    logger.info(f"❌ Policy EXPIRED for {w.id} ({w.name})")
                    notif = NotificationLog(
                        id=f"NTF-{_uuid.uuid4().hex[:8].upper()}",
                        worker_id=w.id,
                        title="❌ Policy Expired",
                        message=f"Your {w.plan.capitalize()} plan expired. Renew now to restore coverage and claim eligibility.",
                        notif_type="plan_change",
                        icon="❌"
                    )
                    db.add(notif)

            elif days_left <= 1 and not w.plan_expiry_notified:
                # ── EXPIRING SOON: send 24hr alert
                w.policy_status = "grace_period"
                w.plan_expiry_notified = True
                alerted_count += 1
                logger.info(f"⚠️  Expiry alert sent for {w.id} ({w.name}) — {int(hours_left)}h left")
                notif = NotificationLog(
                    id=f"NTF-{_uuid.uuid4().hex[:8].upper()}",
                    worker_id=w.id,
                    title="⚠️ Policy Expiring Soon",
                    message=f"Your {w.plan.capitalize()} plan expires in {int(hours_left)} hours on {w.policy_expiry_date.strftime('%d %b %Y')}. Renew to stay protected!",
                    notif_type="plan_change",
                    icon="⚠️"
                )
                db.add(notif)

            elif days_left > 1:
                # ── ACTIVE: reset notification flag for next cycle
                w.policy_status = "active"
                w.is_active = True
                w.plan_expiry_notified = False

        db.commit()
        logger.info(f"✅ Policy lifecycle: {expired_count} expired, {alerted_count} alerted")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error in job_policy_lifecycle: {e}")
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Weekly Maintenance
# ─────────────────────────────────────────────────────────────────────────────

def job_reset_weekly_stats():
    """Weekly Job: Reset all worker hour counters every Sunday at midnight."""
    logger.info("🔄 Task: Resetting weekly stats for all workers...")
    db = SessionLocal()
    try:
        workers = db.query(Worker).all()
        for w in workers:
            w.weekly_hrs_used = 0.0
            w.plan_expiry_notified = False # reset notification flag for new week
        db.commit()
        logger.info(f"✅ Weekly reset complete for {len(workers)} workers")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error in job_reset_weekly_stats: {e}")
    finally:
        db.close()

def initialize_scheduler():
    """Initialize and start background job scheduler."""
    try:
        # Check zone disruptions every 2 minutes (DEMO SPEED)
        scheduler.add_job(
            job_check_zone_disruptions,
            IntervalTrigger(minutes=2),
            id="job_check_zone_disruptions",
            name="Check Zone Disruptions",
            replace_existing=True
        )
        
        # Confirm disruptions every 10 minutes
        scheduler.add_job(
            job_confirm_disruptions,
            IntervalTrigger(minutes=2),
            id="job_confirm_disruptions",
            name="Confirm Disruptions",
            replace_existing=True
        )
        
        # Auto-create claims when disruption confirmed (every 2 minutes)
        scheduler.add_job(
            job_auto_create_claims,
            IntervalTrigger(minutes=2),
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
        
        # Policy lifecycle check — daily at 9 AM
        scheduler.add_job(
            job_policy_lifecycle,
            CronTrigger(hour=9, minute=0),
            id="job_policy_lifecycle",
            name="Policy Lifecycle Auto-Check",
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
        
        # Weekly stats reset — Sunday at 11:59 PM
        scheduler.add_job(
            job_reset_weekly_stats,
            CronTrigger(day_of_week='sun', hour=23, minute=59),
            id="job_reset_weekly_stats",
            name="Weekly Stats Reset",
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
