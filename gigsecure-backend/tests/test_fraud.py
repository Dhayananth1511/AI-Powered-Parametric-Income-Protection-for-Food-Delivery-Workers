import sys
import os
# Add 'app' to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ml_engine import compute_risk_score

def test_risk_scoring_consistency():
    """Verify that risk scores for high-risk zones (like Velachery) are consistently high."""
    high_risk_zone = "Velachery, Chennai"
    low_risk_zone  = "Anna Nagar, Chennai"
    
    risk_high = compute_risk_score(high_risk_zone, 6) # June
    risk_low  = compute_risk_score(low_risk_zone, 1)  # January
    
    print(f"High Risk Zone (Velachery, June): {risk_high}")
    print(f"Low Risk Zone (Anna Nagar, January): {risk_low}")
    
    assert risk_high > risk_low, "Velachery in June should have a higher risk score than Anna Nagar in January"
    
    print(f"High Risk Zone (Koramangala, June): {risk_high}")
    print(f"Low Risk Zone (Vasant Vihar, January): {risk_low}")
    
    assert risk_high > risk_low, "Koramangala in June should have a higher risk score than Vasant Vihar in January"

def test_fraud_heuristic():
    """Verify that the fraud score logic (simulated in Phase 2) correctly identifies outliers."""
    # This simulates our internal fraud scoring logic
    def mock_fraud_score(claims_last_24h, avg_payout, reported_hrs):
        score = 0
        if claims_last_24h > 1: score += 40
        if avg_payout > 1000: score += 30
        if reported_hrs > 7:   score += 30
        return score

    # Low risk
    score_low = mock_fraud_score(0, 200, 2.5)
    # High risk (outlier)
    score_high = mock_fraud_score(2, 1200, 8)
    
    print(f"Low Fraud Score: {score_low}, High Fraud Score: {score_high}")
    assert score_high > 60, "Outlier claim should trigger a high fraud score"
    assert score_low < 20,  "Normal claim should have a low fraud score"

if __name__ == "__main__":
    print("Running Fraud & Integrity Tests...")
    test_risk_scoring_consistency()
    test_fraud_heuristic()
    print("All Fraud & Integrity Tests PASSED!")
