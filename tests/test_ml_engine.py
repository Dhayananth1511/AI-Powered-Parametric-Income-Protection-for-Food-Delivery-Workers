import pytest
from app.ml_engine import compute_risk_score, compute_fraud_score, recommend_plan
from app.models import Worker
import numpy as np

def test_compute_risk_score():
    # If ML mode is loaded, we test the inference
    # Just asserting it returns a non-negative float bound by 0.0 to 1.0
    score = compute_risk_score("Velachery, Chennai")
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

def test_recommend_plan():
    assert recommend_plan(0.1) == "starter"
    assert recommend_plan(0.9) == "elite"
    
def test_compute_fraud_score():
    mock_worker = {"id": "WKR-1234", "trust_score": 90, "claims_approved": 5, "claims_rejected": 0, "zone": "Velachery, Chennai"}
    mock_trigger = {"type": "rainfall"}
    
    result = compute_fraud_score(
        worker_data=mock_worker,
        trigger_data=mock_trigger,
        gps_coordinates=(12.9816, 80.2209),  # Exact match for Velachery
        accelerometer_variance=8.5,
        cell_tower_signal=-75,
        network_latency=45
    )
    
    assert "fraud_score" in result
    assert "decision" in result
    
    score = result["fraud_score"]
    assert 0 <= score <= 100
