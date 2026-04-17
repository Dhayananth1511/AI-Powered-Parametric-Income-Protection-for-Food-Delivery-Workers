from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ── Compliance State (Central Source of Truth) ───────────────────────────────
# In-memory compliance state (survives process restarts via seeding in main.py)
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

def get_compliance_state():
    return _COMPLIANCE_STATE

def update_compliance_state(patch: dict):
    if "market_crash_active" in patch and patch["market_crash_active"] is not None:
        _COMPLIANCE_STATE["market_crash_active"] = patch["market_crash_active"]
    if "new_premium_cap" in patch:
        _COMPLIANCE_STATE["new_premium_cap"] = patch["new_premium_cap"]
    if "new_payout_cap" in patch:
        _COMPLIANCE_STATE["new_payout_cap"] = patch["new_payout_cap"]
    if "sabotage_shield" in patch and patch["sabotage_shield"] is not None:
        _COMPLIANCE_STATE["sabotage_shield"] = patch["sabotage_shield"]
    if "freeze_new_policies" in patch and patch["freeze_new_policies"] is not None:
        _COMPLIANCE_STATE["freeze_new_policies"] = patch["freeze_new_policies"]
    if "emergency_reserve_pct" in patch and patch["emergency_reserve_pct"] is not None:
        _COMPLIANCE_STATE["emergency_reserve_pct"] = patch["emergency_reserve_pct"]
    
    if "note" in patch and patch["note"]:
        _COMPLIANCE_STATE["compliance_notes"].append({
            "text": patch["note"],
            "at": datetime.now().isoformat()
        })
    
    _COMPLIANCE_STATE["last_updated"] = datetime.now().isoformat()
    logger.info(f"🚨 Compliance state updated: crash={_COMPLIANCE_STATE['market_crash_active']}")
    return _COMPLIANCE_STATE

def is_market_crash():
    return _COMPLIANCE_STATE.get("market_crash_active", False)

def get_premium_cap():
    return _COMPLIANCE_STATE.get("new_premium_cap")

def get_payout_cap():
    return _COMPLIANCE_STATE.get("new_payout_cap")

def is_policy_freeze():
    return _COMPLIANCE_STATE.get("freeze_new_policies", False)
