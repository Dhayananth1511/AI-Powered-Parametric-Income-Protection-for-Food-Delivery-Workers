"""
Security Utilities — JWT tokens, password hashing, fraud signals
"""
import os
import jwt
import bcrypt
import logging
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from typing import Optional, Dict
import hashlib
import math

load_dotenv()

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "gigsecure-super-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days

# ─────────────────────────────────────────────────────────────────────────────
# Password Hashing
# ─────────────────────────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# ─────────────────────────────────────────────────────────────────────────────
# JWT Token Management
# ─────────────────────────────────────────────────────────────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        return None

def decode_token(token: str) -> Optional[dict]:
    """Decode token without verification (for debugging only)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        return payload
    except Exception as e:
        logger.error(f"Failed to decode token: {e}")
        return None

# ─────────────────────────────────────────────────────────────────────────────
# 6-Signal Fraud Detection Scoring
# ─────────────────────────────────────────────────────────────────────────────
def compute_multi_signal_fraud_score(
    worker: dict,
    trigger: dict,
    gps_coordinates: Optional[tuple] = None,
    cell_tower_signal: Optional[float] = None,
    network_latency: Optional[float] = None,
) -> Dict[str, float]:
    """
    Compute fraud score using 6 signals:
    1. GPS Consistency (location matches zone)
    2. Accelerometer (motion patterns)
    3. Cell Tower (triangulation match)
    4. Network Quality (spoofing indicator)
    5. Behavioral (trust score + claim history)
    6. Crowd Signal (zone-level validation)
    
    Returns: {fraud_score: 0-100, signals: {}, recommendation: "approve|manual_review|reject"}
    """
    signals = {}
    weights = {
        "gps": 0.25,
        "accelerometer": 0.15,
        "cell_tower": 0.20,
        "network": 0.15,
        "behavioral": 0.15,
        "crowd": 0.10,
    }
    
    # ── Signal 1: GPS Consistency (0-25 points) ──────────────────────────————
    gps_score = _signal_gps_consistency(worker.get("zone", ""), gps_coordinates)
    signals["gps"] = gps_score
    
    # ── Signal 2: Accelerometer (0-15 points) ─────────────────────────────
    accel_score = _signal_accelerometer(trigger)
    signals["accelerometer"] = accel_score
    
    # ── Signal 3: Cell Tower (0-20 points) ──────────────────────────────
    cell_score = _signal_cell_tower(worker.get("zone", ""), cell_tower_signal)
    signals["cell_tower"] = cell_score
    
    # ── Signal 4: Network Quality (0-15 points) ─────────────────────────
    network_score = _signal_network_quality(network_latency)
    signals["network"] = network_score
    
    # ── Signal 5: Behavioral (0-15 points) ──────────────────────────────
    behavioral_score = _signal_behavioral(worker)
    signals["behavioral"] = behavioral_score
    
    # ── Signal 6: Crowd Signal (0-10 points) ────────────────────────────
    crowd_score = _signal_crowd_validation(trigger.get("type", ""))
    signals["crowd"] = crowd_score
    
    # Compute weighted fraud score
    fraud_score = (
        signals["gps"] * weights["gps"] +
        signals["accelerometer"] * weights["accelerometer"] +
        signals["cell_tower"] * weights["cell_tower"] +
        signals["network"] * weights["network"] +
        signals["behavioral"] * weights["behavioral"] +
        signals["crowd"] * weights["crowd"]
    )
    
    # Determine recommendation
    if fraud_score < 20:
        recommendation = "approve"
    elif fraud_score < 50:
        recommendation = "manual_review"
    else:
        recommendation = "reject"
    
    return {
        "fraud_score": round(fraud_score, 1),
        "signals": signals,
        "recommendation": recommendation,
        "reasoning": _generate_fraud_reasoning(signals, fraud_score),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Individual Signal Implementations
# ─────────────────────────────────────────────────────────────────────────────
def _signal_gps_consistency(zone: str, gps_coords: Optional[tuple]) -> float:
    """
    Signal 1: GPS Consistency
    Check if GPS coordinates match zone location.
    Score: 25 points if consistent, 0 if suspicious.
    """
    if not gps_coords:
        return 15.0  # Neutral if no GPS provided
    
    from app.weather import ZONE_COORDS
    
    if zone not in ZONE_COORDS:
        return 15.0  # Can't validate unknown zone
    
    zone_lat, zone_lon = ZONE_COORDS[zone]
    gps_lat, gps_lon = gps_coords
    
    # Calculate distance using Haversine formula
    distance_km = _haversine(gps_lat, gps_lon, zone_lat, zone_lon)
    
    # 0-5km = good (25 points), 5-10km = okay (15 points), >10km = suspicious (0 points)
    if distance_km <= 5:
        return 25.0
    elif distance_km <= 10:
        return 15.0
    else:
        return 0.0

def _signal_accelerometer(trigger: dict) -> float:
    """
    Signal 2: Accelerometer Motion Pattern
    Heavy rainfall/extreme heat should show movement patterns.
    Score: 15 points if consistent with trigger type.
    """
    trigger_type = trigger.get("type", "")
    
    # If disruption is confirmed (e.g., heavy rain), expect erratic movement
    # For now, give full score if trigger is valid (in real app, check sensor data)
    if trigger_type in ["rainfall", "temperature", "aqi", "cyclone", "curfew"]:
        return 15.0
    else:
        return 5.0

def _signal_cell_tower(zone: str, signal_strength: Optional[float]) -> float:
    """
    Signal 3: Cell Tower Triangulation
    Cross-validate zone location using cell tower signal strength.
    Score: 20 points if consistent.
    """
    if not signal_strength:
        return 12.0  # Neutral if no signal data
    
    # Strong signal (>-100dBm) in expected zone = good (20 points)
    # Weak signal (<-120dBm) = suspicious (5 points)
    if signal_strength > -100:
        return 20.0
    elif signal_strength > -120:
        return 12.0
    else:
        return 5.0

def _signal_network_quality(latency_ms: Optional[float]) -> float:
    """
    Signal 4: Network Quality & Connection Stability
    Spoofing typically shows network artifacts (jitter, high latency).
    Score: 15 points if network is stable.
    """
    if not latency_ms:
        return 10.0  # Neutral if no latency data
    
    # Good network (<100ms) = 15 points
    # Okay network (100-200ms) = 10 points
    # Bad network (>200ms) = 5 points
    if latency_ms < 100:
        return 15.0
    elif latency_ms < 200:
        return 10.0
    else:
        return 5.0

def _signal_behavioral(worker: dict) -> float:
    """
    Signal 5: Behavioral Profile & History
    Check trust score and claim patterns.
    Score: 15 points if good history, 0 if suspicious.
    """
    trust_score = worker.get("trust_score", 40)
    claims_approved = worker.get("claims_approved", 0)
    claims_rejected = worker.get("claims_rejected", 0)
    
    # High trust score = good behavior
    trust_component = (trust_score / 100) * 8  # Up to 8 points
    
    # Rejection rate
    total_claims = claims_approved + claims_rejected
    if total_claims > 0:
        rejection_rate = claims_rejected / total_claims
        rejection_component = (1 - min(rejection_rate, 1)) * 7  # Up to 7 points
    else:
        rejection_component = 6.0  # Neutral for new users
    
    return round(trust_component + rejection_component, 1)

def _signal_crowd_validation(trigger_type: str) -> float:
    """
    Signal 6: Crowd Signal Validation
    In real implementation, check if multiple workers in zone reported same disruption.
    For now, simulate based on trigger type consistency.
    Score: 10 points if crowd confirms trigger.
    """
    # All trigger types are valid for now
    # In production, query disruption_events table for zone confirmation
    return 10.0

# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────
def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points on Earth (in km)."""
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def _generate_fraud_reasoning(signals: dict, fraud_score: float) -> str:
    """Generate human-readable fraud detection reasoning."""
    reasons = []
    
    if signals.get("gps", 0) < 10:
        reasons.append("GPS location inconsistent with reported zone")
    if signals.get("cell_tower", 0) < 10:
        reasons.append("Cell tower signal weak")
    if signals.get("network", 0) < 10:
        reasons.append("Network quality degraded")
    if signals.get("behavioral", 0) < 5:
        reasons.append("Behavioral pattern unusual")
    
    if not reasons:
        if fraud_score < 20:
            return "All signals consistent. Disruption appears genuine."
        elif fraud_score < 50:
            return "Some signals unclear. Recommend manual review."
        else:
            return "Multiple signals inconsistent. Possible fraud attempt."
    
    return " | ".join(reasons)

# ─────────────────────────────────────────────────────────────────────────────
# Request Signing (for API calls)
# ─────────────────────────────────────────────────────────────────────────────
def sign_request(data: dict, secret: str) -> str:
    """Sign request data for API verification."""
    import json
    message = json.dumps(data, sort_keys=True)
    signature = hashlib.sha256((message + secret).encode()).hexdigest()
    return signature
