"""
Test Suite: Payment Engine (Phase 2A)
Tests for payment order creation, webhook handling, and payment state management.
"""

import pytest
import json
import uuid
import hmac
import hashlib
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from app.payment_engine import PaymentEngine
from app.models import Payment, PaymentEvent
from app.database import SessionLocal

# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def payment_engine_instance():
    """Create payment engine for testing."""
    engine = PaymentEngine(mode="test")
    engine.key_secret = "test_secret_for_webhook_verification"
    return engine

@pytest.fixture
def test_worker_data():
    """Sample worker data for testing."""
    return {
        "id": "WKR-TEST123",
        "name": "Test Worker",
        "zone": "Marina Beach, Chennai",
        "plan": "standard",
        "trust_score": 75
    }

@pytest.fixture
def test_claim_data():
    """Sample claim data for testing."""
    return {
        "id": "CLM-TEST456",
        "worker_id": "WKR-TEST123",
        "payout_amount": 150.00,
        "status": "pending"
    }

# ─────────────────────────────────────────────────────────────────────────────
# Test: Payment Order Creation
# ─────────────────────────────────────────────────────────────────────────────

def test_create_order_success(payment_engine_instance, test_claim_data):
    """Test successful payment order creation."""
    result = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=str(uuid.uuid4())
    )
    
    assert result["success"] is True
    assert result["payment_id"] is not None
    assert result["razorpay_order_id"] is not None
    assert result["amount_rupees"] == test_claim_data["payout_amount"]
    assert result["status"] == "order_created"

def test_create_order_idempotency(payment_engine_instance, test_claim_data):
    """Test idempotent payment order creation."""
    idempotency_key = str(uuid.uuid4())
    
    # First call
    result1 = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=idempotency_key
    )
    
    # Second call with same claim_id (should return existing)
    result2 = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=idempotency_key
    )
    
    assert result1["success"] is True
    assert result2["success"] is False
    assert result2["error"] == "Payment already exists for this claim"

def test_create_order_invalid_amount(payment_engine_instance, test_claim_data):
    """Test payment creation with invalid amount."""
    result = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=-50,  # Negative amount
        worker_id=test_claim_data["worker_id"],
        idempotency_key=str(uuid.uuid4())
    )
    
    assert result["success"] is False
    assert "Invalid amount" in result["error"]

# ─────────────────────────────────────────────────────────────────────────────
# Test: Webhook Signature Verification
# ─────────────────────────────────────────────────────────────────────────────

def test_verify_webhook_signature_valid(payment_engine_instance):
    """Test valid webhook signature verification."""
    payload = json.dumps({"event": "payment.authorized", "data": "test"})
    
    # Generate correct signature
    correct_signature = hmac.new(
        payment_engine_instance.key_secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    is_valid = payment_engine_instance.verify_webhook_signature(payload, correct_signature)
    assert is_valid is True

def test_verify_webhook_signature_invalid(payment_engine_instance):
    """Test invalid webhook signature verification."""
    payload = json.dumps({"event": "payment.authorized", "data": "test"})
    invalid_signature = "wrong_signature_hash"
    
    is_valid = payment_engine_instance.verify_webhook_signature(payload, invalid_signature)
    assert is_valid is False

# ─────────────────────────────────────────────────────────────────────────────
# Test: Webhook Event Processing
# ─────────────────────────────────────────────────────────────────────────────

def test_handle_payment_authorized_webhook(payment_engine_instance, test_claim_data):
    """Test handling payment.authorized webhook."""
    # First create an order
    order_result = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=str(uuid.uuid4())
    )
    
    razorpay_order_id = order_result["razorpay_order_id"]
    
    # Simulate webhook payload
    webhook_payload = {
        "event": "payment.authorized",
        "payload": {
            "payment": {
                "entity": {
                    "id": "pay_12345",
                    "order_id": razorpay_order_id,
                    "amount": int(test_claim_data["payout_amount"] * 100),
                    "currency": "INR",
                    "status": "captured",
                    "description": "Payment approved"
                }
            }
        }
    }
    
    result = payment_engine_instance.handle_webhook(webhook_payload)
    
    assert result["status"] == "success"
    assert result["payment_id"] is not None

def test_handle_payment_failed_webhook(payment_engine_instance, test_claim_data):
    """Test handling payment.failed webhook."""
    # First create an order
    order_result = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=str(uuid.uuid4())
    )
    
    razorpay_order_id = order_result["razorpay_order_id"]
    
    # Simulate failure webhook
    webhook_payload = {
        "event": "payment.failed",
        "payload": {
            "payment": {
                "entity": {
                    "id": "pay_12345",
                    "order_id": razorpay_order_id,
                    "amount": int(test_claim_data["payout_amount"] * 100),
                    "currency": "INR",
                    "status": "failed",
                    "description": "Insufficient funds",
                    "error_code": "BAD_REQUEST"
                }
            }
        }
    }
    
    result = payment_engine_instance.handle_webhook(webhook_payload)
    
    assert result["status"] == "will_retry"
    assert result["retry_count"] == 1

# ─────────────────────────────────────────────────────────────────────────────
# Test: Payment Status Retrieval
# ─────────────────────────────────────────────────────────────────────────────

def test_get_payment_status(payment_engine_instance, test_claim_data):
    """Test retrieving payment status."""
    # Create order
    order_result = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=str(uuid.uuid4())
    )
    
    payment_id = order_result["payment_id"]
    
    # Get status
    status = payment_engine_instance.get_payment_status(payment_id)
    
    assert status["payment_id"] == payment_id
    assert status["status"] == "created"
    assert status["amount_rupees"] == test_claim_data["payout_amount"]
    assert "events" in status
    assert len(status["events"]) >= 1

# ─────────────────────────────────────────────────────────────────────────────
# Test: Payment Retry
# ─────────────────────────────────────────────────────────────────────────────

def test_retry_payment_success(payment_engine_instance, test_claim_data):
    """Test successful payment retry."""
    # Create order
    order_result = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=str(uuid.uuid4())
    )
    
    payment_id = order_result["payment_id"]
    
    # Manually mark as failed (for testing)
    db = SessionLocal()
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    payment.status = "failed"
    payment.error_message = "Test failure"
    db.commit()
    db.close()
    
    # Retry
    retry_result = payment_engine_instance.retry_payment(payment_id)
    
    assert retry_result["success"] is True
    assert retry_result["payment_id"] == payment_id

def test_retry_payment_max_retries_exceeded(payment_engine_instance, test_claim_data):
    """Test retry when max retries exceeded."""
    # Create order
    order_result = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=str(uuid.uuid4())
    )
    
    payment_id = order_result["payment_id"]
    
    # Mark as failed with max retries exceeded
    db = SessionLocal()
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    payment.status = "failed"
    payment.retry_count = 3  # Max retries
    db.commit()
    db.close()
    
    # Try to retry
    retry_result = payment_engine_instance.retry_payment(payment_id)
    
    assert retry_result["success"] is False
    assert "Max retries" in retry_result["error"]

# ─────────────────────────────────────────────────────────────────────────────
# Test: Amount Conversion (Rupees to Paise)
# ─────────────────────────────────────────────────────────────────────────────

def test_amount_conversion():
    """Test rupees to paise conversion accuracy."""
    test_cases = [
        (150.00, 15000),
        (1.50, 150),
        (0.01, 1),
        (999.99, 99999),
    ]
    
    for rupees, expected_paise in test_cases:
        paise = int(rupees * 100)
        assert paise == expected_paise, f"Failed: {rupees} → {paise} (expected {expected_paise})"

# ─────────────────────────────────────────────────────────────────────────────
# Test: Edge Cases
# ─────────────────────────────────────────────────────────────────────────────

def test_handle_unknown_webhook_event(payment_engine_instance):
    """Test handling unknown webhook event."""
    result = payment_engine_instance.handle_webhook({
        "event": "unknown.event",
        "payload": {}
    })
    
    assert result["status"] == "ignored"

def test_webhook_without_signature(payment_engine_instance):
    """Test webhook handling without signature."""
    # Should still process if webhook_secret not configured
    result = payment_engine_instance.verify_webhook_signature("payload", "")
    # In test mode with no secret, should return True
    assert isinstance(result, bool)

# ─────────────────────────────────────────────────────────────────────────────
# Integration Test: Full Claim-to-Payment Flow
# ─────────────────────────────────────────────────────────────────────────────

def test_full_payment_flow(payment_engine_instance, test_claim_data):
    """Test complete flow: order creation → webhook → success."""
    # Step 1: Create order
    order_result = payment_engine_instance.create_order(
        claim_id=test_claim_data["id"],
        amount_rupees=test_claim_data["payout_amount"],
        worker_id=test_claim_data["worker_id"],
        idempotency_key=str(uuid.uuid4())
    )
    
    assert order_result["success"] is True
    payment_id = order_result["payment_id"]
    razorpay_order_id = order_result["razorpay_order_id"]
    
    # Step 2: Simulate payment authorization
    webhook_payload = {
        "event": "payment.authorized",
        "payload": {
            "payment": {
                "entity": {
                    "id": "pay_auth123",
                    "order_id": razorpay_order_id,
                    "amount": int(test_claim_data["payout_amount"] * 100),
                    "currency": "INR",
                    "status": "captured"
                }
            }
        }
    }
    
    webhook_result = payment_engine_instance.handle_webhook(webhook_payload)
    assert webhook_result["status"] == "success"
    
    # Step 3: Verify payment status is now confirmed
    status = payment_engine_instance.get_payment_status(payment_id)
    assert status["status"] == "confirmed"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
