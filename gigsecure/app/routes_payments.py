"""
Payment Routes — Phase 2A
Endpoints for payment creation, webhook handling, and status checks.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import json
import logging
from app.payment_engine import payment_engine
from app.database import SessionLocal
from app.models import Payment, Claim
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/claims", tags=["payments"])

# ─────────────────────────────────────────────────────────────────────────────
# Payment Order Creation
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/{claim_id}/payment/create")
async def create_payment_order(claim_id: str, body: dict = None):
    """
    Create Razorpay payment order for a claim.
    
    Request:
        {
            "idempotency_key": "unique-uuid"  # Optional but recommended
        }
    
    Response:
        {
            "success": bool,
            "payment_id": str,
            "razorpay_order_id": str,
            "amount_rupees": float,
            "status": str,
            "checkout_url": str
        }
    """
    if body is None:
        body = {}
    
    db = SessionLocal()
    try:
        # Get claim
        claim = db.query(Claim).filter(Claim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        # Verify claim is approved (has payout amount)
        if claim.payout_amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Claim has no payout amount; cannot create payment"
            )
        
        # Generate idempotency key if not provided
        idempotency_key = (
            body.get("idempotency_key") or 
            f"{claim_id}__{datetime.utcnow().isoformat()}"
        )
        
        # Create order via payment engine
        result = payment_engine.create_order(
            claim_id=claim_id,
            amount_rupees=claim.payout_amount,
            worker_id=claim.worker_id,
            idempotency_key=idempotency_key
        )
        
        return JSONResponse(result)
    
    except HTTPException as e:
        logger.error(f"HTTP error creating payment: {e}")
        raise
    except Exception as e:
        logger.error(f"Error creating payment order: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Razorpay Webhook Handler
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/payment/webhook")
async def razorpay_webhook(request: Request):
    """
    Razorpay webhook endpoint.
    Receives payment events and updates claim status.
    
    Authenticates using signature verification.
    """
    try:
        # Get raw request body for signature verification
        body = await request.body()
        body_str = body.decode("utf-8")
        
        # Get signature header
        signature = request.headers.get("X-Razorpay-Signature")
        if not signature:
            logger.warning("❌ Webhook received without signature")
            return JSONResponse({"status": "error", "message": "Missing signature"}, status_code=400)
        
        # Verify signature
        if not payment_engine.verify_webhook_signature(body_str, signature):
            logger.warning("❌ Invalid webhook signature")
            return JSONResponse({"status": "error", "message": "Invalid signature"}, status_code=403)
        
        # Parse event data
        event_data = json.loads(body_str)
        
        # Process webhook
        result = payment_engine.handle_webhook(event_data)
        
        logger.info(f"✅ Webhook processed: {result}")
        return JSONResponse(result)
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON in webhook")
        return JSONResponse({"status": "error", "message": "Invalid JSON"}, status_code=400)
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# ─────────────────────────────────────────────────────────────────────────────
# Payment Status
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/{claim_id}/payment/status")
async def get_payment_status(claim_id: str):
    """
    Get payment status and event history for a claim.
    
    Response:
        {
            "payment_id": str,
            "claim_id": str,
            "status": str,
            "amount_rupees": float,
            "retry_count": int,
            "error": str or null,
            "created_at": str,
            "events": [
                {
                    "event_type": str,
                    "timestamp": str,
                    "data": dict
                }
            ]
        }
    """
    db = SessionLocal()
    try:
        # Find payment for this claim
        payment = db.query(Payment).filter(Payment.claim_id == claim_id).first()
        if not payment:
            return JSONResponse({
                "status": "not_found",
                "message": "No payment found for this claim"
            }, status_code=404)
        
        # Get payment details
        result = payment_engine.get_payment_status(payment.id)
        return JSONResponse(result)
    
    except Exception as e:
        logger.error(f"Error getting payment status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# ─────────────────────────────────────────────────────────────────────────────
# Manual Payment Retry (Admin Only)
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/payment/{payment_id}/retry")
async def retry_payment(payment_id: str):
    """
    Manually retry a failed payment.
    (In production, add admin authorization check)
    
    Response:
        {
            "success": bool,
            "payment_id": str,
            "error": str (if failure)
        }
    """
    try:
        result = payment_engine.retry_payment(payment_id)
        status_code = 200 if result.get("success") else 400
        return JSONResponse(result, status_code=status_code)
    except Exception as e:
        logger.error(f"Error retrying payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ─────────────────────────────────────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/payment/health")
async def payment_health():
    """
    Check payment system health.
    """
    return JSONResponse({
        "status": "healthy",
        "razorpay_configured": payment_engine.client is not None,
        "mode": payment_engine.mode
    })
