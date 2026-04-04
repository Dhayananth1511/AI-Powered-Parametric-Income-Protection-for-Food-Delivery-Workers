import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest

# Define output directory
output_dir = os.path.join(os.path.dirname(__file__), "app", "models_bin")
os.makedirs(output_dir, exist_ok=True)

print("🚀 Starting ZenVyte GigPulse ML Training Script...")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Train Zone Risk Classifier (Random Forest)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1/2] Generating Synthetic Risk Data...")
np.random.seed(42)
num_samples = 15000

# Features: flood_risk, proximity_water, elevation, aqi_history, disruption_months, month_of_year
X_risk = []
y_risk = []

for _ in range(num_samples):
    flood_risk = np.random.uniform(0.1, 0.9)
    proximity_water = np.random.uniform(0.1, 0.9)
    elevation = np.random.uniform(0.1, 0.9)  # Higher is safer
    aqi_history = np.random.uniform(0.2, 0.8)
    disruption_months = np.random.uniform(1, 10) / 12.0
    month = np.random.randint(1, 13)
    
    monsoon_boost = 0.15 if month in [6, 7, 8, 9] else 0.0
    
    score = (
        flood_risk * 0.35 +
        proximity_water * 0.25 +
        (1 - elevation) * 0.15 +
        aqi_history * 0.10 +
        disruption_months * 0.15 +
        monsoon_boost
    )
    
    # Add noise to make the ML model actually learn
    score = min(max(score + np.random.normal(0, 0.05), 0.0), 1.0)
    
    X_risk.append([flood_risk, proximity_water, elevation, aqi_history, disruption_months, month])
    
    # Categorize into 5 plans
    if score < 0.25: plan_class = 0    # Starter
    elif score < 0.45: plan_class = 1  # Basic
    elif score < 0.60: plan_class = 2  # Standard
    elif score < 0.75: plan_class = 3  # Premium
    else: plan_class = 4               # Elite
        
    y_risk.append(plan_class)

X_risk = np.array(X_risk)
y_risk = np.array(y_risk)

print(f"Training RandomForestClassifier on {num_samples} records...")
risk_model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
risk_model.fit(X_risk, y_risk)

risk_model_path = os.path.join(output_dir, "zone_risk_model.pkl")
joblib.dump(risk_model, risk_model_path)
print(f"✅ Saved Zone Risk Model -> {risk_model_path}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Train Fraud Detection Engine (Isolation Forest)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2/2] Generating Synthetic Fraud Data...")
# We use Isolation Forest for anomaly detection. Normal behavior is the inlier (+1), fraud is outlier (-1).

# Features: gps_dist_km, motion_variance, signal_strength_dbm, latency_ms, trust_score
num_fraud_samples = 20000

X_fraud = []
for _ in range(num_fraud_samples):
    is_fraud = np.random.random() < 0.05  # 5% are actual fraudsters

    if is_fraud:
        gps_dist = np.random.uniform(5.0, 50.0) # Far away from zone
        motion_var = np.random.uniform(0.0, 0.5) # Stationary (spoofing)
        signal = np.random.uniform(-130, -110) # Weak signal / home Wi-Fi mismatch
        latency = np.random.uniform(150, 500) # High latency (VPN/Spoofer)
        trust = np.random.uniform(0, 50) # Lower trust
    else:
        gps_dist = np.random.uniform(0.0, 3.5) # Inside micro-zone
        motion_var = np.random.uniform(2.5, 15.0) # Moving/shaking bike
        signal = np.random.uniform(-95, -60) # Strong cell tower
        latency = np.random.uniform(20, 90) # Good latency
        trust = np.random.uniform(40, 100) # Average to high trust

    X_fraud.append([gps_dist, motion_var, signal, latency, trust])

X_fraud = np.array(X_fraud)

print(f"Training IsolationForest on {num_fraud_samples} records...")
fraud_model = IsolationForest(contamination=0.06, random_state=42, n_estimators=100)
fraud_model.fit(X_fraud)

fraud_model_path = os.path.join(output_dir, "fraud_detection_model.pkl")
joblib.dump(fraud_model, fraud_model_path)
print(f"✅ Saved Fraud Detection Model -> {fraud_model_path}")

print("\n🎉 ML Training Complete! You can now launch ZenVyte GigPulse.")
