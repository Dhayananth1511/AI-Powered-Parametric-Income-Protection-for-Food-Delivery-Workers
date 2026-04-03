import sys
import os
# Add 'app' to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ml_engine import calculate_dynamic_premium, PLAN_BASE

def test_premium_scaling():
    """Verify that premiums scale correctly with plan levels."""
    plans = ["starter", "basic", "standard", "premium", "elite"]
    zone = "Indiranagar, Bengaluru"
    month = 6 # June (Monsoon)
    
    prev_premium = 0
    for p in plans:
        res = calculate_dynamic_premium(zone, p, month)
        premium = res["final_premium"]
        print(f"Plan: {p} -> Premium: {premium}")
        assert premium > prev_premium, f"Premium for {p} should be higher than previous plan"
        prev_premium = premium

def test_monsoon_impact():
    """Verify that monsoon months increase the premium for high-risk zones."""
    zone = "Koromangala, Bengaluru"
    plan = "standard"
    
    june_res = calculate_dynamic_premium(zone, plan, 6) # Monsoon
    oct_res  = calculate_dynamic_premium(zone, plan, 10) # Off-season
    
    print(f"June Premium: {june_res['final_premium']}, Oct Premium: {oct_res['final_premium']}")
    assert june_res["final_premium"] > oct_res["final_premium"], "Monsoon premium should be higher due to seasonal adjustment"

def test_trust_discount():
    """Verify that trust scores reduce the final premium."""
    zone = "HSR Layout, Bengaluru"
    plan = "premium"
    
    no_trust_res = calculate_dynamic_premium(zone, plan, 5, trust_score=0)
    high_trust_res = calculate_dynamic_premium(zone, plan, 5, trust_score=90)
    
    print(f"No Trust: {no_trust_res['final_premium']}, High Trust: {high_trust_res['final_premium']}")
    assert high_trust_res["final_premium"] < no_trust_res["final_premium"], "High trust score should result in a lower premium"

if __name__ == "__main__":
    print("Running Actuarial Tests...")
    test_premium_scaling()
    test_monsoon_impact()
    test_trust_discount()
    print("All Actuarial Tests PASSED!")
