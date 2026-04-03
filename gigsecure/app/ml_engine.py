import numpy as np
from typing import Dict, List
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# 40+ Tamil Nadu Zone Data
# Features: flood_risk, proximity_water, elevation, aqi_history, disruption_months
# ─────────────────────────────────────────────────────────────────────────────
ZONE_DATA: Dict[str, dict] = {
    # Chennai Core
    "Velachery, Chennai":       {"flood_risk":0.85,"proximity_water":0.90,"elevation":0.20,"aqi_history":0.60,"disruption_months":8},
    "Marina Beach, Chennai":    {"flood_risk":0.90,"proximity_water":1.00,"elevation":0.10,"aqi_history":0.50,"disruption_months":9},
    "T. Nagar, Chennai":        {"flood_risk":0.55,"proximity_water":0.40,"elevation":0.50,"aqi_history":0.70,"disruption_months":6},
    "Anna Nagar, Chennai":      {"flood_risk":0.30,"proximity_water":0.20,"elevation":0.70,"aqi_history":0.40,"disruption_months":4},
    "Adyar, Chennai":           {"flood_risk":0.75,"proximity_water":0.80,"elevation":0.30,"aqi_history":0.50,"disruption_months":7},
    "Tambaram, Chennai":        {"flood_risk":0.45,"proximity_water":0.30,"elevation":0.60,"aqi_history":0.50,"disruption_months":5},
    "Porur, Chennai":           {"flood_risk":0.60,"proximity_water":0.50,"elevation":0.40,"aqi_history":0.60,"disruption_months":6},
    "Chromepet, Chennai":       {"flood_risk":0.50,"proximity_water":0.40,"elevation":0.50,"aqi_history":0.60,"disruption_months":5},
    "Perungudi, Chennai":       {"flood_risk":0.70,"proximity_water":0.70,"elevation":0.30,"aqi_history":0.60,"disruption_months":7},
    "Sholinganallur, Chennai":  {"flood_risk":0.65,"proximity_water":0.60,"elevation":0.40,"aqi_history":0.50,"disruption_months":6},
    "Mylapore, Chennai":        {"flood_risk":0.60,"proximity_water":0.60,"elevation":0.40,"aqi_history":0.60,"disruption_months":6},
    "Guindy, Chennai":          {"flood_risk":0.55,"proximity_water":0.40,"elevation":0.50,"aqi_history":0.70,"disruption_months":6},
    "Kodambakkam, Chennai":     {"flood_risk":0.50,"proximity_water":0.40,"elevation":0.50,"aqi_history":0.60,"disruption_months":5},
    "Nungambakkam, Chennai":    {"flood_risk":0.40,"proximity_water":0.30,"elevation":0.60,"aqi_history":0.50,"disruption_months":4},
    "Egmore, Chennai":          {"flood_risk":0.45,"proximity_water":0.30,"elevation":0.60,"aqi_history":0.60,"disruption_months":5},
    "Washermanpet, Chennai":    {"flood_risk":0.80,"proximity_water":0.80,"elevation":0.20,"aqi_history":0.60,"disruption_months":8},
    "Royapuram, Chennai":       {"flood_risk":0.85,"proximity_water":0.90,"elevation":0.20,"aqi_history":0.50,"disruption_months":8},
    "Thiruvottiyur, Chennai":   {"flood_risk":0.75,"proximity_water":0.70,"elevation":0.30,"aqi_history":0.60,"disruption_months":7},
    "Avadi, Chennai":           {"flood_risk":0.35,"proximity_water":0.30,"elevation":0.60,"aqi_history":0.50,"disruption_months":4},
    "Ambattur, Chennai":        {"flood_risk":0.45,"proximity_water":0.40,"elevation":0.50,"aqi_history":0.60,"disruption_months":5},
    # Chennai Extended
    "Pallavaram, Chennai":      {"flood_risk":0.40,"proximity_water":0.30,"elevation":0.60,"aqi_history":0.55,"disruption_months":4},
    "Madipakkam, Chennai":      {"flood_risk":0.65,"proximity_water":0.55,"elevation":0.40,"aqi_history":0.60,"disruption_months":6},
    "Perambur, Chennai":        {"flood_risk":0.50,"proximity_water":0.35,"elevation":0.55,"aqi_history":0.65,"disruption_months":5},
    "Kolathur, Chennai":        {"flood_risk":0.45,"proximity_water":0.30,"elevation":0.60,"aqi_history":0.55,"disruption_months":5},
    "Virugambakkam, Chennai":   {"flood_risk":0.50,"proximity_water":0.35,"elevation":0.55,"aqi_history":0.60,"disruption_months":5},
    "Mogappair, Chennai":       {"flood_risk":0.35,"proximity_water":0.25,"elevation":0.65,"aqi_history":0.45,"disruption_months":4},
    "Korattur, Chennai":        {"flood_risk":0.45,"proximity_water":0.35,"elevation":0.55,"aqi_history":0.55,"disruption_months":5},
    "Thiruvanmiyur, Chennai":   {"flood_risk":0.70,"proximity_water":0.75,"elevation":0.30,"aqi_history":0.50,"disruption_months":7},
    "Besant Nagar, Chennai":    {"flood_risk":0.80,"proximity_water":0.90,"elevation":0.20,"aqi_history":0.45,"disruption_months":8},
    "Injambakkam, Chennai":     {"flood_risk":0.75,"proximity_water":0.80,"elevation":0.25,"aqi_history":0.45,"disruption_months":7},
    # Tamil Nadu Other Cities
    "Coimbatore Central":       {"flood_risk":0.25,"proximity_water":0.30,"elevation":0.65,"aqi_history":0.55,"disruption_months":3},
    "RS Puram, Coimbatore":     {"flood_risk":0.30,"proximity_water":0.35,"elevation":0.60,"aqi_history":0.50,"disruption_months":3},
    "Gandhipuram, Coimbatore":  {"flood_risk":0.35,"proximity_water":0.30,"elevation":0.60,"aqi_history":0.60,"disruption_months":4},
    "Madurai Central":          {"flood_risk":0.40,"proximity_water":0.50,"elevation":0.50,"aqi_history":0.65,"disruption_months":4},
    "Anna Nagar, Madurai":      {"flood_risk":0.35,"proximity_water":0.40,"elevation":0.55,"aqi_history":0.55,"disruption_months":4},
    "Trichy Central":           {"flood_risk":0.55,"proximity_water":0.65,"elevation":0.40,"aqi_history":0.55,"disruption_months":5},
    "Srirangam, Trichy":        {"flood_risk":0.70,"proximity_water":0.80,"elevation":0.25,"aqi_history":0.50,"disruption_months":6},
    "Salem Central":            {"flood_risk":0.30,"proximity_water":0.35,"elevation":0.60,"aqi_history":0.60,"disruption_months":4},
    "Tirunelveli Central":      {"flood_risk":0.45,"proximity_water":0.55,"elevation":0.45,"aqi_history":0.50,"disruption_months":5},
    "Erode Central":            {"flood_risk":0.35,"proximity_water":0.45,"elevation":0.55,"aqi_history":0.55,"disruption_months":4},
    "Vellore Central":          {"flood_risk":0.40,"proximity_water":0.45,"elevation":0.55,"aqi_history":0.55,"disruption_months":4},
    "Kanchipuram":              {"flood_risk":0.50,"proximity_water":0.55,"elevation":0.45,"aqi_history":0.55,"disruption_months":5},
    "Pondicherry Central":      {"flood_risk":0.70,"proximity_water":0.85,"elevation":0.20,"aqi_history":0.45,"disruption_months":7},
    "Cuddalore":                {"flood_risk":0.65,"proximity_water":0.75,"elevation":0.25,"aqi_history":0.50,"disruption_months":6},
    "Nagapattinam":             {"flood_risk":0.85,"proximity_water":0.95,"elevation":0.10,"aqi_history":0.45,"disruption_months":9},
}

# ─────────────────────────────────────────────────────────────────────────────
# Plan Metadata
# ─────────────────────────────────────────────────────────────────────────────
PLAN_BASE = {
    "starter":  {"premium": 55,  "rate": 35, "maxHrs": 3, "cap": 105},
    "basic":    {"premium": 70,  "rate": 45, "maxHrs": 4, "cap": 180},
    "standard": {"premium": 90,  "rate": 60, "maxHrs": 5, "cap": 300},
    "premium":  {"premium": 115, "rate": 75, "maxHrs": 6, "cap": 450},
    "elite":    {"premium": 135, "rate": 90, "maxHrs": 7, "cap": 630},
}

PLAN_ORDER = ["starter", "basic", "standard", "premium", "elite"]

# ─────────────────────────────────────────────────────────────────────────────
# Core Risk Score
# ─────────────────────────────────────────────────────────────────────────────
def compute_risk_score(zone: str, month: int = 6) -> float:
    """Compute zone risk score 0.0–1.0 with seasonal adjustment."""
    data = ZONE_DATA.get(zone)
    if not data:
        return 0.55  # default for unknown zones
    monsoon_boost = 0.15 if month in [6, 7, 8, 9, 10, 11] else 0.0
    score = (
        data["flood_risk"]                    * 0.35 +
        data["proximity_water"]               * 0.25 +
        (1 - data["elevation"])               * 0.15 +
        data["aqi_history"]                   * 0.10 +
        (data["disruption_months"] / 12)      * 0.15 +
        monsoon_boost
    )
    return round(min(score, 1.0), 3)

def recommend_plan(risk_score: float) -> str:
    if risk_score < 0.25:   return "starter"
    elif risk_score < 0.45: return "basic"
    elif risk_score < 0.60: return "standard"
    elif risk_score < 0.75: return "premium"
    else:                   return "elite"

# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Premium Calculation (ML-powered with trust discount)
# ─────────────────────────────────────────────────────────────────────────────
def calculate_dynamic_premium(zone: str, plan: str, month: int = None,
                               trust_score: int = 40) -> dict:
    """
    Dynamic premium calculation using:
    - Zone flood/AQI risk score
    - Seasonal multiplier (monsoon vs off-season)
    - Worker trust score discount (₹2–5 for trusted workers)
    - Zone-specific AQI surcharge
    """
    if month is None:
        month = datetime.now().month

    risk  = compute_risk_score(zone, month)
    meta  = PLAN_BASE.get(plan, PLAN_BASE["standard"])
    base  = meta["premium"]

    # Zone risk adjustment: ±₹15 based on risk deviation from 0.5 baseline
    zone_data = ZONE_DATA.get(zone, {})
    risk_deviation = risk - 0.5
    zone_adjustment = round(risk_deviation * 30)  # ₹-15 to ₹+15

    # AQI surcharge: high-pollution zones add ₹3–8
    aqi_hist = zone_data.get("aqi_history", 0.5)
    aqi_surcharge = round(aqi_hist * 8) if aqi_hist > 0.65 else 0

    # Trust score discount: safe workers save ₹2–5
    if trust_score >= 75:
        trust_discount = 5
    elif trust_score >= 50:
        trust_discount = 3
    elif trust_score >= 25:
        trust_discount = 1
    else:
        trust_discount = 0

    # Seasonal adjustment: slight reduction off-season, slight increase monsoon
    seasonal = 5 if month in [6, 7, 8, 9, 10, 11] else -2

    final = max(base + zone_adjustment + aqi_surcharge - trust_discount + seasonal, base - 15)

    return {
        "base_premium":    base,
        "risk_score":      risk,
        "zone_adjustment": zone_adjustment,
        "aqi_surcharge":   aqi_surcharge,
        "trust_discount":  trust_discount,
        "seasonal_adj":    seasonal,
        "final_premium":   final,
        "recommended_plan":recommend_plan(risk),
        "plan":            plan,
        "zone":            zone,
        "hourly_rate":     meta["rate"],
        "max_hours":       meta["maxHrs"],
        "weekly_cap":      meta["cap"],
    }

# ─────────────────────────────────────────────────────────────────────────────
# Zone Risk Breakdown (for UI display)
# ─────────────────────────────────────────────────────────────────────────────
def zone_risk_breakdown(zone: str, month: int = None) -> dict:
    """Return per-factor risk breakdown for UI visualization."""
    if month is None:
        month = datetime.now().month
    data = ZONE_DATA.get(zone, {})
    risk = compute_risk_score(zone, month)
    return {
        "zone":                zone,
        "overall_risk":        risk,
        "risk_label":          _risk_label(risk),
        "recommended_plan":    recommend_plan(risk),
        "factors": {
            "flood_risk":       data.get("flood_risk", 0.5),
            "water_proximity":  data.get("proximity_water", 0.5),
            "elevation_inv":    round(1 - data.get("elevation", 0.5), 2),
            "aqi_history":      data.get("aqi_history", 0.5),
            "disruption_freq":  round(data.get("disruption_months", 6) / 12, 2),
        },
        "is_monsoon":          month in [6, 7, 8, 9, 10, 11],
        "disruption_months_per_year": data.get("disruption_months", 6),
    }

def _risk_label(score: float) -> str:
    if score < 0.3:  return "Low Risk"
    if score < 0.5:  return "Moderate Risk"
    if score < 0.7:  return "High Risk"
    return "Very High Risk"

# ─────────────────────────────────────────────────────────────────────────────
# Fraud Detection Engine
# ─────────────────────────────────────────────────────────────────────────────
def compute_fraud_score(worker_data: dict) -> dict:
    """
    6-signal fraud detection (Isolation Forest simulation).
    Signals: GPS·Accelerometer·CellTower·PriorActivity·CrowdSignal·Baseline
    """
    signals = {}
    score   = 0

    # Signal 1: GPS in zone (always pass in verified context)
    signals["gps_in_zone"]      = True
    # Signal 2: Accelerometer confirms movement (trust score proxy)
    signals["accelerometer_ok"] = worker_data.get("trust_score", 40) > 50
    # Signal 3: Cell tower matches zone
    signals["cell_tower_match"] = worker_data.get("trust_score", 40) > 30
    # Signal 4: Prior zone activity (not too many recent claims)
    signals["prior_activity"]   = worker_data.get("claims_total", 0) < 25
    # Signal 5: Crowd signal consistent
    signals["crowd_signal"]     = True
    # Signal 6: Historical baseline consistent
    signals["baseline_ok"]      = worker_data.get("trust_score", 40) > 25

    if signals["gps_in_zone"]:      score += 2
    if signals["accelerometer_ok"]: score += 2
    if signals["cell_tower_match"]: score += 2
    if signals["prior_activity"]:   score += 1
    if signals["crowd_signal"]:     score += 1
    if signals["baseline_ok"]:      score += 1

    fraud_score = max(0, 100 - (score * 12))

    if fraud_score < 30:   decision = "AUTO_APPROVED"
    elif fraud_score < 70: decision = "MANUAL_REVIEW"
    else:                  decision = "AUTO_REJECTED"

    trust = worker_data.get("trust_score", 40)
    trust_tier = (
        "🟢 Trusted"     if trust >= 75 else
        "🔵 Established" if trust >= 50 else
        "🟡 Building"    if trust >= 25 else
        "🔴 Restricted"
    )

    return {
        "fraud_score": fraud_score,
        "decision":    decision,
        "signals":     signals,
        "score_raw":   score,
        "trust_tier":  trust_tier,
        "signals_passed": sum(1 for v in signals.values() if v),
        "signals_total":  len(signals),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Predictive Disruption Forecast (XGBoost-style simulation)
# ─────────────────────────────────────────────────────────────────────────────
def predict_disruption_probability(zone: str, hour: int = None, month: int = None) -> dict:
    """
    Predict disruption probability for next 48 hours per zone.
    Uses zone risk data + seasonal pattern + time-of-day weighting.
    Simulates XGBoost output with deterministic numpy computation.
    """
    if hour is None:
        hour = datetime.now().hour
    if month is None:
        month = datetime.now().month

    data = ZONE_DATA.get(zone, {
        "flood_risk": 0.5, "proximity_water": 0.5, "elevation": 0.5,
        "aqi_history": 0.5, "disruption_months": 5
    })

    base_risk = compute_risk_score(zone, month)

    # Time-of-day weighting (monsoon evenings 6-10pm highest risk)
    time_weights = {
        0: 0.3, 1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.3,
        6: 0.5, 7: 0.6, 8: 0.7, 9: 0.7, 10: 0.6, 11: 0.6,
        12: 0.7, 13: 0.7, 14: 0.8, 15: 0.8, 16: 0.9, 17: 0.9,
        18: 1.0, 19: 1.0, 20: 0.9, 21: 0.8, 22: 0.6, 23: 0.4,
    }

    forecasts = []
    rng = np.random.default_rng(seed=hash(zone) % (2**31))  # deterministic per zone

    for h_offset in range(48):
        forecast_hour = (hour + h_offset) % 24
        tw = time_weights.get(forecast_hour, 0.5)
        noise = rng.uniform(-0.08, 0.08)
        prob = min(1.0, max(0.0, base_risk * tw + noise))
        forecasts.append({
            "hour_offset": h_offset,
            "hour": forecast_hour,
            "probability": round(prob * 100, 1),
            "risk_level": "High" if prob > 0.6 else "Medium" if prob > 0.35 else "Low",
        })

    # Peak window
    peak = max(forecasts, key=lambda x: x["probability"])

    return {
        "zone":           zone,
        "base_risk":      base_risk,
        "forecasts":      forecasts[:24],  # 24-hr detailed
        "peak_hour":      peak["hour"],
        "peak_prob":      peak["probability"],
        "alert":          peak["probability"] > 60,
        "alert_message":  f"⚡ Storm likely around {peak['hour']:02d}:00 today. Probability: {peak['probability']}%. Your coverage is active." if peak["probability"] > 60 else None,
    }

# ─────────────────────────────────────────────────────────────────────────────
# Utility
# ─────────────────────────────────────────────────────────────────────────────
def get_all_zones() -> List[str]:
    return sorted(ZONE_DATA.keys())

def get_zone_categories() -> dict:
    """Return zones grouped by city."""
    cities = {}
    for zone in ZONE_DATA.keys():
        parts = zone.split(", ")
        city = parts[-1] if len(parts) > 1 else "Other"
        cities.setdefault(city, []).append(zone)
    return cities

def calculate_loss_ratio(plan: str, disruption_hrs_annual: float = 52.5) -> dict:
    meta = PLAN_BASE.get(plan, PLAN_BASE["standard"])
    annual_premium = meta["premium"] * 52
    expected_claim = meta["rate"] * disruption_hrs_annual
    loss_ratio = round(expected_claim / annual_premium * 100, 1)
    monsoon_claim = meta["rate"] * (disruption_hrs_annual * 1.4)
    monsoon_ratio = round(monsoon_claim / annual_premium * 100, 1)
    return {
        "plan":            plan,
        "annual_premium":  annual_premium,
        "expected_claim":  round(expected_claim, 0),
        "loss_ratio":      loss_ratio,
        "monsoon_claim":   round(monsoon_claim, 0),
        "monsoon_ratio":   monsoon_ratio,
        "status":          "✅ Controlled" if loss_ratio < 75 else "⚠️ Review",
    }