import time
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Worker, Claim
from app.ml_engine import compute_risk_score

def verify_worker_integrity(worker_id: str):
    """
    Background task to scan worker behaviors for anomalies.
    Simulates a real-time 'Integrity Scan' that looks at sensors and history.
    """
    db: Session = SessionLocal()
    try:
        worker = db.query(Worker).filter(Worker.id == worker_id).first()
        if not worker:
            return

        print(f"[TASK] Starting Integrity Scan for {worker.name} ({worker_id})...")
        
        # Simulate ML Model (Isolation Forest) processing time
        time.sleep(2) 
        
        # Anomaly Detection Logic (Simulated Phase 3)
        # In a real system, this would query sensor_logs table
        anomaly_detected = False
        
        # Scenario: If trust score is low and they have many recent claims
        if worker.trust_score < 30 and worker.claims_total > 5:
            # 10% chance to flag for high-res audit
            if random.random() < 0.1:
                anomaly_detected = True
        
        if anomaly_detected:
            print(f"[ALERT] Anomaly detected for {worker.id}. Reducing trust score.")
            worker.trust_score = max(0, worker.trust_score - 5)
        else:
            # Reward consistency
            if random.random() < 0.05:
                worker.trust_score = min(100, worker.trust_score + 1)
        
        db.commit()
        print(f"[TASK] Integrity Scan complete for {worker.id}. New Trust Score: {worker.trust_score}")
        
    except Exception as e:
        print(f"[ERROR] Integrity Scan failed: {e}")
    finally:
        db.close()
