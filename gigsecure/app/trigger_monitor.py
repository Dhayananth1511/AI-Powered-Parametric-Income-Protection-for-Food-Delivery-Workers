"""
Trigger Monitor — 5-parametric-trigger confirmation engine
Tracks disruption events per zone with 15–30 min confirmation windows.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict
from app.models import DisruptionEvent, NotificationLog, Worker
from app.database import SessionLocal
import asyncio, uuid

# ─────────────────────────────────────────────────────────────────────────────
# In-memory confirmation state (zone → event state)
# ─────────────────────────────────────────────────────────────────────────────
_ZONE_STATE: Dict[str, dict] = {}

CONFIRMATION_MINUTES = 20   # 15–30 min window (20 for demo)

def _db():
    return SessionLocal()

# ─────────────────────────────────────────────────────────────────────────────
# Check current zone status
# ─────────────────────────────────────────────────────────────────────────────
def get_zone_status(zone: str) -> dict:
    """Return current trigger status for a zone."""
    state = _ZONE_STATE.get(zone)
    if not state:
        return {
            "zone":   zone,
            "status": "monitoring",
            "label":  "All Clear",
            "triggers": [],
            "payout_active": False,
        }

    now = datetime.now()
    trigger = state.get("trigger", {})
    conf_start = state.get("confirmation_start")

    if state["status"] == "monitoring":
        return {
            "zone":   zone,
            "status": "monitoring",
            "label":  "Monitoring — No Disruption",
            "triggers": [],
            "payout_active": False,
        }

    if state["status"] == "confirming":
        elapsed = (now - conf_start).total_seconds() / 60 if conf_start else 0
        remaining = max(0, CONFIRMATION_MINUTES - elapsed)
        pct = min(100, (elapsed / CONFIRMATION_MINUTES) * 100)
        return {
            "zone":   zone,
            "status": "confirming",
            "label":  f"⏳ Confirming — {int(remaining)}min remaining",
            "trigger": trigger,
            "elapsed_min": round(elapsed, 1),
            "remaining_min": round(remaining, 1),
            "confirmation_pct": round(pct, 0),
            "triggers": [trigger],
            "payout_active": False,
        }

    if state["status"] == "confirmed":
        conf_end = state.get("confirmation_end")
        disruption_hrs = (now - conf_end).total_seconds() / 3600 if conf_end else 0
        return {
            "zone":   zone,
            "status": "confirmed",
            "label":  f"⚡ DISRUPTION ACTIVE — {trigger.get('label', 'Alert')}",
            "trigger": trigger,
            "disruption_hrs": round(disruption_hrs, 2),
            "event_id": state.get("event_id"),
            "triggers": [trigger],
            "payout_active": True,
        }

    return {"zone": zone, "status": "cleared", "label": "Disruption Cleared", "triggers": [], "payout_active": False}

# ─────────────────────────────────────────────────────────────────────────────
# Start a confirmation window for a zone trigger
# ─────────────────────────────────────────────────────────────────────────────
def start_confirmation_window(zone: str, trigger: dict) -> dict:
    """Begin 15–30 min confirmation window. Store in DB and memory."""
    now = datetime.now()
    event_id = "DSR-" + uuid.uuid4().hex[:8].upper()

    _ZONE_STATE[zone] = {
        "status":             "confirming",
        "trigger":            trigger,
        "confirmation_start": now,
        "event_id":           event_id,
    }

    # Persist to DB
    db = _db()
    try:
        evt = DisruptionEvent(
            id            = event_id,
            zone          = zone,
            trigger_type  = trigger["type"],
            trigger_value = float(trigger.get("value", 0)),
            trigger_label = trigger.get("label", ""),
            status        = "confirming",
            confirmation_start = now,
            payout_type   = trigger.get("payout_type", "hourly"),
        )
        db.add(evt)
        db.commit()
    finally:
        db.close()

    return {
        "event_id":   event_id,
        "zone":       zone,
        "status":     "confirming",
        "trigger":    trigger,
        "will_confirm_at": (now + timedelta(minutes=CONFIRMATION_MINUTES)).isoformat(),
    }

def confirm_disruption(zone: str) -> Optional[dict]:
    """Mark a confirming disruption as confirmed (threshold persisted)."""
    state = _ZONE_STATE.get(zone)
    if not state or state["status"] != "confirming":
        return None

    now = datetime.now()
    state["status"]           = "confirmed"
    state["confirmation_end"] = now
    event_id = state.get("event_id")

    # Update DB
    db = _db()
    try:
        evt = db.query(DisruptionEvent).filter(DisruptionEvent.id == event_id).first()
        if evt:
            evt.status           = "confirmed"
            evt.confirmation_end = now
            db.commit()

        # Notify all workers in this zone
        workers = db.query(Worker).filter(Worker.zone == zone, Worker.is_active == True).all()
        trigger = state["trigger"]
        for w in workers:
            notif = NotificationLog(
                worker_id  = w.id,
                title      = f"⚡ {trigger.get('label', 'Disruption')} in Your Zone",
                message    = f"Disruption confirmed in {zone}. Auto-claim initiated. Payout coming shortly.",
                notif_type = "disruption_alert",
                icon       = "🌧️" if trigger["type"] == "rainfall" else "🔥" if trigger["type"] == "temperature" else "💨" if trigger["type"] == "aqi" else "🌀",
            )
            db.add(notif)
        db.commit()
    finally:
        db.close()

    return {"zone": zone, "status": "confirmed", "event_id": event_id}

def clear_disruption(zone: str) -> dict:
    """Clear a confirmed/confirming disruption (event ended)."""
    state = _ZONE_STATE.pop(zone, {})
    event_id = state.get("event_id")
    if event_id:
        db = _db()
        try:
            evt = db.query(DisruptionEvent).filter(DisruptionEvent.id == event_id).first()
            if evt:
                evt.status = "cleared"
                db.commit()
        finally:
            db.close()
    return {"zone": zone, "status": "cleared"}

# ─────────────────────────────────────────────────────────────────────────────
# Simulate a disruption (for demo/testing)
# ─────────────────────────────────────────────────────────────────────────────
def simulate_disruption(zone: str, trigger_type: str = "rainfall") -> dict:
    """
    Simulate a full disruption lifecycle for demo purposes.
    Goes through: monitoring → confirming → confirmed
    The frontend can poll zone-status to see progression.
    """
    TRIGGER_MAP = {
        "rainfall":    {"type": "rainfall",    "value": 42.0, "label": "Heavy Rainfall",  "payout_type": "hourly",   "unit": "mm"},
        "temperature": {"type": "temperature", "value": 44.5, "label": "Extreme Heat",    "payout_type": "hourly",   "unit": "°C"},
        "aqi":         {"type": "aqi",         "value": 320,  "label": "Severe AQI",      "payout_type": "hourly",   "unit": "AQI"},
        "cyclone":     {"type": "cyclone",     "value": 1,    "label": "Cyclone Alert",   "payout_type": "full_cap", "unit": "alert"},
        "curfew":      {"type": "curfew",      "value": 1,    "label": "Curfew/Hartal",  "payout_type": "full_cap", "unit": "flag"},
    }
    trigger = TRIGGER_MAP.get(trigger_type, TRIGGER_MAP["rainfall"])

    # For demo: instantly set to confirmed (skip 20-min wait)
    now = datetime.now()
    event_id = "DSR-" + uuid.uuid4().hex[:8].upper()

    _ZONE_STATE[zone] = {
        "status":             "confirmed",
        "trigger":            trigger,
        "confirmation_start": now - timedelta(minutes=CONFIRMATION_MINUTES),
        "confirmation_end":   now,
        "event_id":           event_id,
    }

    db = _db()
    try:
        evt = DisruptionEvent(
            id                 = event_id,
            zone               = zone,
            trigger_type       = trigger["type"],
            trigger_value      = float(trigger["value"]),
            trigger_label      = trigger["label"],
            status             = "confirmed",
            confirmation_start = now - timedelta(minutes=CONFIRMATION_MINUTES),
            confirmation_end   = now,
            payout_type        = trigger["payout_type"],
        )
        db.add(evt)
        db.commit()
    finally:
        db.close()

    return {
        "event_id":  event_id,
        "zone":      zone,
        "status":    "confirmed",
        "trigger":   trigger,
        "simulated": True,
    }

# ─────────────────────────────────────────────────────────────────────────────
# Get all active disruption events
# ─────────────────────────────────────────────────────────────────────────────
def get_active_events() -> list:
    """Return all zones currently in confirming or confirmed state."""
    events = []
    for zone, state in _ZONE_STATE.items():
        if state["status"] in ["confirming", "confirmed"]:
            events.append({
                "zone":      zone,
                "status":    state["status"],
                "trigger":   state.get("trigger", {}),
                "event_id":  state.get("event_id"),
            })
    return events

def get_all_disruption_events_db(limit: int = 50) -> list:
    """Fetch recent disruption events from DB."""
    db = _db()
    try:
        events = db.query(DisruptionEvent).order_by(DisruptionEvent.created_at.desc()).limit(limit).all()
        return [
            {
                "id": e.id, "zone": e.zone, "trigger_type": e.trigger_type,
                "trigger_value": e.trigger_value, "trigger_label": e.trigger_label,
                "status": e.status, "payout_type": e.payout_type,
                "disruption_hrs": e.disruption_hrs, "workers_affected": e.workers_affected,
                "created_at": str(e.created_at),
            }
            for e in events
        ]
    finally:
        db.close()
