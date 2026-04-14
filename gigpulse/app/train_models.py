import os
import sys
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest

print("🚀 Starting ML Model Training Pipeline...")

# Ensure directories exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models_bin")
os.makedirs(MODELS_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Train Zone Risk Classifier (Random Forest)
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Generating synthetic data for Zone Risk Model...")
# Features: [flood_risk, proximity_water, elevation, aqi_history, disruption_freq, month]
np.random.seed(42)
n_samples = 2500

flood_risk = np.random.uniform(0.1, 0.95, n_samples)
proximity = np.random.uniform(0.1, 0.95, n_samples)
elevation = np.random.uniform(0.1, 0.9, n_samples)
aqi = np.random.uniform(0.3, 0.8, n_samples)
freq = np.random.uniform(0.1, 1.0, n_samples)
months = np.random.randint(1, 13, n_samples)

X_risk = np.column_stack([flood_risk, proximity, elevation, aqi, freq, months])

# Target: 0 (Low), 1 (Basic), 2 (Standard), 3 (Premium), 4 (Elite)
def generate_risk_label(row):
    f, p, e, a, fr, m = row
    monsoon_boost = 0.2 if m in [6,7,8,9,10,11] else 0.0
    score = (f * 0.35) + (p * 0.25) + ((1 - e) * 0.15) + (a * 0.10) + (fr * 0.15) + monsoon_boost
    
    if score < 0.35: return 0
    elif score < 0.50: return 1
    elif score < 0.65: return 2
    elif score < 0.80: return 3
    else: return 4

y_risk = np.array([generate_risk_label(row) for row in X_risk])

print("🤖 Training Random Forest Classifier...")
rf_model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
rf_model.fit(X_risk, y_risk)

rf_path = os.path.join(MODELS_DIR, "zone_risk_model.pkl")
joblib.dump(rf_model, rf_path)
print(f"✅ Zone Risk Model saved to {rf_path}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Train Fraud Detection Engine (Isolation Forest)
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Generating synthetic telemetry for Fraud Model...")
# Features: [gps_distance_km, motion_variance, signal_dbm, network_latency_ms, trust_score]

n_normal = 3000
n_fraud = 500

# Normal profiles (Real Workers)
# Close to zone center (0-3km), high motion (vibration), good signal, good trust
X_normal = np.column_stack([
    np.random.gamma(2.0, 0.5, n_normal),            # gps dist (km)
    np.random.normal(5.5, 1.5, n_normal),           # motion variance (vibrating bike)
    np.random.normal(-75, 10, n_normal),            # signal dBm
    np.random.lognormal(4.0, 0.3, n_normal),        # latency (ms)
    np.random.normal(70, 15, n_normal)              # trust score
])

# Fraud profiles (GPS Spoofers)
# Exactly at center (0km) or very far, Zero motion (flat), awful signal (home WiFi often hides cell), low trust
X_fraud = np.column_stack([
    np.random.choice([0.0, np.random.uniform(10, 50)], n_fraud), # gps spoofed to exact 0.0 or failed and shows far
    np.random.normal(0.1, 0.05, n_fraud),           # flat motion (phone sitting on desk)
    np.random.normal(-110, 5, n_fraud),             # weak/hidden cell tower
    np.random.lognormal(5.5, 0.5, n_fraud),         # high latency from spoofing proxy
    np.random.normal(30, 10, n_fraud)               # low trust
])

X_fraud_combined = np.vstack([X_normal, X_fraud])

print("🤖 Training Isolation Forest...")
if_model = IsolationForest(n_estimators=150, contamination=float(n_fraud)/len(X_fraud_combined), random_state=42)
if_model.fit(X_fraud_combined)

if_path = os.path.join(MODELS_DIR, "fraud_detection_model.pkl")
joblib.dump(if_model, if_path)
print(f"✅ Fraud Detection Model saved to {if_path}")

print("🎉 ML Pipeline complete. Ready for Soar Phase.")
