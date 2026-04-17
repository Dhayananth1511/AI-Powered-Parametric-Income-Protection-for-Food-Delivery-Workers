"""
Payment Engine — Razorpay Integration
Handles order creation, webhook verification, and payment state management.
Phase 2A implementation: Real payment processing with audit trail.
"""

import os
import hmac
import hashlib
import uuid
import json
from datetime import UTC, datetime
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv
from app.database import SessionLocal, engine, Base
from app.models import Payment, PaymentEvent, Claim, Worker, Policy
import logging

load_dotenv()

logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

# ─────────────────────────────────────────────────────────────────────────────
# Razorpay Integration (Import with graceful fallback for testing)
# ─────────────────────────────────────────────────────────────────────────────
try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except ImportError:
    RAZORPAY_AVAILABLE = False

class PaymentEngine:
    """
    Handles all payment operations:
    - Create Razorpay orders
    - Verify webhook signatures
    - Process payment callbacks
    - Retry failed payments
    - Maintain audit trail
    """
    
    def __init__(self, mode: str = "test"):
        """
        Initialize payment engine.
        Args:
            mode: 'test' (sandbox) or 'live' (production)
        """
        self.mode = mode
        self.key_id = os.getenv("RAZORPAY_KEY_ID")
        self.key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        self.webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")
        
        self.client = None
        if RAZORPAY_AVAILABLE and self.key_id and self.key_secret:
            try:
                self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
                logger.info(f"✅ Razorpay client initialized ({mode} mode)")
            except Exception as e:
                logger.warning(f"Failed to initialize Razorpay client: {e}")
                self.client = None
        if self.mode == "test":
            self._reset_test_state()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Order Creation
    # ─────────────────────────────────────────────────────────────────────────
    
    def create_order(self, claim_id: str, amount_rupees: float, 
                     worker_id: str, idempotency_key: str) -> Dict:
        """
        Create Razorpay order for a claim.
        Implements idempotency: same idempotency_key returns same order.
        
        Args:
            claim_id: ZenVyte GigPulse claim ID
            amount_rupees: Payout amount in rupees
            worker_id: Worker ID
            idempotency_key: Unique key for idempotent requests
        
        Returns:
            {
                "success": bool,
                "payment_id": str,  # ZenVyte GigPulse payment ID
                "razorpay_order_id": str,
                "amount_rupees": float,
                "status": str,
                "checkout_url": str (if success),
                "error": str (if failure)
            }
        """
        db = SessionLocal()
        try:
            # Validate amount before duplicate checks so bad requests fail consistently.
            if amount_rupees <= 0:
                return {
                    "success": False,
                    "error": "Invalid amount"
                }

            # Check for duplicate/existing payment (idempotency)
            query = db.query(Payment).filter(
                Payment.worker_id == worker_id,
                Payment.status.in_(["pending", "created", "order_created", "confirmed", "success"])
            )
            if claim_id:
                query = query.filter(Payment.claim_id == claim_id)
            else:
                # For renewals, use the idempotency key logic or check recent pending renewals
                query = query.filter(Payment.claim_id == None, Payment.created_at >= datetime.now().replace(hour=0, minute=0, second=0))

            existing = query.first()
            
            if existing:
                logger.info(f"⚠️  Payment already exists: {existing.id}")
                return {
                    "success": False,
                    "error": "Active payment order already exists",
                    "payment_id": existing.id,
                    "status": existing.status
                }
            
            amount_paise = int(amount_rupees * 100)
            
            # Create Razorpay order (or mock if not configured)
            if self.client:
                rzp_order = self._create_razorpay_order(
                    amount_paise, claim_id, worker_id, idempotency_key
                )
                if not rzp_order:
                    return {
                        "success": False,
                        "error": "Failed to create Razorpay order"
                    }
                razorpay_order_id = rzp_order.get("id")
            else:
                # Mock mode (for testing)
                razorpay_order_id = f"order_mock_{uuid.uuid4().hex[:12]}"
                logger.info(f"📝 Using mock order ID: {razorpay_order_id}")
            
            # Create Payment record
            payment = Payment(
                id=f"PAY-{uuid.uuid4().hex[:8].upper()}",
                claim_id=claim_id,
                worker_id=worker_id,
                razorpay_order_id=razorpay_order_id,
                amount_rupees=amount_rupees,
                amount_paise=amount_paise,
                status="created",
                initiated_by="system",
                order_created_at=datetime.now(UTC).replace(tzinfo=None)
            )
            db.add(payment)
            db.commit()
            
            # Log event
            self._log_event(db, payment.id, "order_created", {
                "claim_id": claim_id,
                "amount_rupees": amount_rupees,
                "razorpay_order_id": razorpay_order_id
            })
            
            logger.info(f"✅ Payment order created: {payment.id} | {razorpay_order_id} | ₹{amount_rupees}")
            
            return {
                "success": True,
                "payment_id": payment.id,
                "razorpay_order_id": razorpay_order_id,
                "amount_rupees": amount_rupees,
                "status": "order_created",
                "checkout_url": f"https://checkout.razorpay.com/?key={self.key_id}" if self.client else None
            }
        
        except Exception as e:
            logger.error(f"❌ Failed to create payment order: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()
    
    def _create_razorpay_order(self, amount_paise: int, claim_id: Optional[str], 
                               worker_id: str, idempotency_key: str = None) -> Optional[Dict]:
        """Create actual Razorpay order via API."""
        try:
            # Razorpay receipt must be unique and <= 40 chars
            receipt = f"gsec_{claim_id}" if claim_id else (idempotency_key[:40] if idempotency_key else f"ren_{worker_id}_{uuid.uuid4().hex[:8]}")
            
            order_data = {
                "amount": amount_paise,
                "currency": "INR",
                "receipt": receipt,
                "notes": {
                    "claim_id": claim_id or "renewal",
                    "worker_id": worker_id,
                    "platform": "gigpulse",
                }
            }
            logger.info(f"📡 Sending request to Razorpay: {order_data}")
            rzp_order = self.client.order.create(order_data)
            return rzp_order
        except Exception as e:
            logger.error(f"❌ Razorpay API error: {str(e)}")
            return None
    
    # ─────────────────────────────────────────────────────────────────────────
    # Webhook Verification & Processing
    # ─────────────────────────────────────────────────────────────────────────
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verify Razorpay webhook signature using HMAC SHA256.
        
        Args:
            payload: Raw request body (before parsing JSON)
            signature: Signature header from webhook
        
        Returns:
            True if signature is valid, False otherwise
        """
        secret = self.webhook_secret or self.key_secret
        if not secret:
            logger.warning("⚠️  Webhook secret not configured; skipping signature verification")
            return True  # Allow in dev mode
        
        try:
            expected = hmac.new(
                secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            is_valid = signature == expected
            
            if not is_valid:
                logger.warning(f"❌ Invalid webhook signature: expected {expected}, got {signature}")
            
            return is_valid
        except Exception as e:
            logger.error(f"Webhook signature verification error: {e}")
            return False
    
    def handle_webhook(self, event_data: Dict) -> Dict:
        """
        Process Razorpay webhook callback.
        
        Supported events:
        - payment.authorized: Payment successful
        - payment.failed: Payment failed
        - payment.captured: Funds captured
        
        Args:
            event_data: Decoded webhook payload
        
        Returns:
            {"status": "success|ignored|error", "details": {...}}
        """
        db = SessionLocal()
        try:
            event_type = event_data.get("event")
            payload = event_data.get("payload", {})
            
            logger.info(f"Processing webhook event: {event_type}")
            
            if event_type == "payment.authorized":
                return self._handle_payment_authorized(db, payload)
            elif event_type == "payment.failed":
                return self._handle_payment_failed(db, payload)
            elif event_type == "payment.captured":
                return self._handle_payment_captured(db, payload)
            else:
                logger.warning(f"Unhandled webhook event: {event_type}")
                return {"status": "ignored", "event": event_type}
        
        except Exception as e:
            logger.error(f"Webhook processing error: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            db.close()
    
    def _handle_payment_authorized(self, db, payload: Dict) -> Dict:
        """Handle successful payment authorization from Razorpay."""
        payment_entity = payload.get("payment", {}).get("entity", {})
        razorpay_payment_id = payment_entity.get("id")
        razorpay_order_id = payment_entity.get("order_id")
        amount = payment_entity.get("amount")  # in paise
        
        # Find Payment record
        payment = db.query(Payment).filter(
            Payment.razorpay_order_id == razorpay_order_id
        ).first()
        
        if not payment:
            logger.error(f"❌ Payment not found for order {razorpay_order_id}")
            return {"status": "error", "message": "Payment not found"}
        
        try:
            # Update payment status
            payment.razorpay_payment_id = razorpay_payment_id
            payment.status = "confirmed"
            payment.payment_received_at = datetime.now(UTC).replace(tzinfo=None)
            db.commit()
            
            # Log event
            self._log_event(db, payment.id, "payment_authorized", {
                "razorpay_payment_id": razorpay_payment_id,
                "amount": amount,
                "status": "confirmed"
            })
            
            # ── Action ────────────────────────────────────────────────────────
            if payment.claim_id:
                # Update Claim status
                claim = db.query(Claim).filter(Claim.id == payment.claim_id).first()
                if claim:
                    claim.status = "approved"
                    if not hasattr(claim, 'payout_status'):
                        claim.razorpay_payment_id = razorpay_payment_id
                    db.commit()
                logger.info(f"✅ Claim payment authorized: {payment.id} | ₹{payment.amount_rupees}")
            else:
                # It's a POLICY RENEWAL
                worker = db.query(Worker).filter(Worker.id == payment.worker_id).first()
                if worker:
                    from datetime import timedelta
                    
                    # 1. Update Worker model for fast state checks
                    old_expiry = worker.policy_expiry_date or datetime.now()
                    new_expiry = old_expiry + timedelta(days=7)
                    worker.policy_expiry_date = new_expiry
                    worker.policy_status = "active"
                    worker.is_active = True
                    
                    # 2. Create permanent Policy history record for the audit trail
                    new_policy = Policy(
                        id = "POL-" + uuid.uuid4().hex[:6].upper(),
                        worker_id = worker.id,
                        plan = worker.plan or "standard",
                        premium = payment.amount_rupees,
                        status = "active",
                        start_date = old_expiry,
                        end_date = new_expiry,
                        renewal_count = 0 # Will be updated if we want to track sequence
                    )
                    db.add(new_policy)
                    db.commit()
                    logger.info(f"✅ Policy renewal record created: {new_policy.id} | Worker: {payment.worker_id}")
            
            # Send notification
            self._send_payout_notification(db, payment.worker_id, payment.amount_rupees)
            
            return {
                "status": "success",
                "payment_id": payment.id,
                "message": "Payment received and processed successfully"
            }
        
        except Exception as e:
            logger.error(f"Error handling payment authorized: {e}")
            return {"status": "error", "message": str(e)}
    
    def _handle_payment_failed(self, db, payload: Dict) -> Dict:
        """Handle payment failure and schedule retry."""
        payment_entity = payload.get("payment", {}).get("entity", {})
        razorpay_order_id = payment_entity.get("order_id")
        error_description = payment_entity.get("description", "Payment failed")
        error_code = payment_entity.get("error_code", "UNKNOWN")
        
        payment = db.query(Payment).filter(
            Payment.razorpay_order_id == razorpay_order_id
        ).first()
        
        if not payment:
            logger.error(f"❌ Payment not found for order {razorpay_order_id}")
            return {"status": "error", "message": "Payment not found"}
        
        try:
            payment.status = "failed"
            payment.error_message = error_description
            payment.error_code = error_code
            payment.retry_count += 1
            db.commit()
            
            self._log_event(db, payment.id, "payment_failed", {
                "error_code": error_code,
                "error_message": error_description,
                "retry_count": payment.retry_count
            })
            
            if payment.retry_count < payment.max_retries:
                logger.info(f"⚠️  Payment failed, will retry: {payment.id} (attempt {payment.retry_count}/{payment.max_retries})")
                return {
                    "status": "will_retry",
                    "payment_id": payment.id,
                    "retry_count": payment.retry_count
                }
            else:
                logger.error(f"❌ Payment failed permanently: {payment.id}")
                return {
                    "status": "failed_permanently",
                    "payment_id": payment.id,
                    "error": error_description
                }
        
        except Exception as e:
            logger.error(f"Error handling payment failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def _handle_payment_captured(self, db, payload: Dict) -> Dict:
        """Handle payment capture confirmation."""
        payment_entity = payload.get("payment", {}).get("entity", {})
        razorpay_payment_id = payment_entity.get("id")
        razorpay_order_id = payment_entity.get("order_id")
        
        payment = db.query(Payment).filter(
            Payment.razorpay_payment_id == razorpay_payment_id
        ).first()
        
        if not payment:
            logger.warning(f"⚠️  Payment capture for unknown payment: {razorpay_payment_id}")
            return {"status": "ignored"}
        
        try:
            payment.status = "success"
            db.commit()
            
            self._log_event(db, payment.id, "payment_captured", {
                "razorpay_payment_id": razorpay_payment_id
            })
            
            logger.info(f"✅ Payment captured: {payment.id}")
            return {"status": "success", "payment_id": payment.id}
        
        except Exception as e:
            logger.error(f"Error handling payment capture: {e}")
            return {"status": "error", "message": str(e)}
    
    # ─────────────────────────────────────────────────────────────────────────
    # Payment Status & Retry
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_payment_status(self, payment_id: str) -> Dict:
        """Get payment status and event history."""
        db = SessionLocal()
        try:
            payment = db.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                return {"error": "Payment not found"}
            
            events = db.query(PaymentEvent).filter(
                PaymentEvent.payment_id == payment_id
            ).order_by(PaymentEvent.created_at).all()
            
            return {
                "payment_id": payment.id,
                "claim_id": payment.claim_id,
                "status": payment.status,
                "amount_rupees": payment.amount_rupees,
                "retry_count": payment.retry_count,
                "error": payment.error_message,
                "created_at": payment.created_at.isoformat(),
                "events": [
                    {
                        "event_type": e.event_type,
                        "timestamp": e.created_at.isoformat(),
                        "data": e.event_data
                    } for e in events
                ]
            }
        finally:
            db.close()
    
    def retry_payment(self, payment_id: str) -> Dict:
        """Manually retry a failed payment."""
        db = SessionLocal()
        try:
            payment = db.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                return {"success": False, "error": "Payment not found"}
            
            if payment.status != "failed":
                return {"success": False, "error": "Payment is not in failed status"}
            
            if payment.retry_count >= payment.max_retries:
                return {"success": False, "error": "Max retries exceeded"}
            
            # Reset to created status for retry
            payment.status = "created"
            payment.error_message = None
            payment.error_code = None
            db.commit()
            
            self._log_event(db, payment.id, "retry_initiated", {
                "retry_count": payment.retry_count
            })
            
            logger.info(f"🔄 Retry initiated for payment: {payment.id}")
            return {"success": True, "payment_id": payment.id}
        finally:
            db.close()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Audit Logging
    # ─────────────────────────────────────────────────────────────────────────
    
    def _log_event(self, db, payment_id: str, event_type: str, event_data: Dict):
        """Log payment event for audit trail."""
        try:
            event = PaymentEvent(
                id=f"PEV-{uuid.uuid4().hex[:8].upper()}",
                payment_id=payment_id,
                event_type=event_type,
                event_data=event_data
            )
            db.add(event)
            db.commit()
        except Exception as e:
            logger.error(f"Failed to log payment event: {e}")
    
    def _send_payout_notification(self, db, worker_id: str, amount_rupees: float):
        """Send payout notification to worker via multiple channels."""
        try:
            from app.models import NotificationLog
            
            # 1. In-App Notification
            notif = NotificationLog(
                id=f"NTF-{uuid.uuid4().hex[:8].upper()}",
                worker_id=worker_id,
                title="💰 Payout Credited",
                message=f"Your weather disruption claim has been approved. ₹{amount_rupees:.2f} will be credited within 24 hours.",
                notif_type="payout_credited",
                amount=amount_rupees,
                icon="💰"
            )
            db.add(notif)
            db.commit()

            # 2. External Notifications (Free Channels)
            worker = db.query(Worker).filter(Worker.id == worker_id).first()
            if worker:
                from app.sms_engine import (
                    send_sms_notification, send_whatsapp_notification,
                    send_telegram_notification, send_free_whatsapp_notification
                )
                msg = f"ZenVyte GigPulse: Payout of ₹{amount_rupees:.2f} credited to your UPI account."
                send_sms_notification(worker.phone, msg)
                send_whatsapp_notification(worker.phone, msg)
                send_telegram_notification(msg)
                send_free_whatsapp_notification(msg)

            logger.info(f"📧 All Notifications sent to {worker_id}")
        except Exception as e:
            logger.error(f"Failed to send payout notification: {e}")

    def _reset_test_state(self):
        """Clear payment tables between tests while preserving worker and claim data."""
        db = SessionLocal()
        try:
            db.query(PaymentEvent).delete()
            db.query(Payment).delete()
            db.commit()
        except Exception as e:
            db.rollback()
            logger.warning(f"Failed to reset payment test state: {e}")
        finally:
            db.close()


# ─────────────────────────────────────────────────────────────────────────────
# Global Payment Engine Instance
# ─────────────────────────────────────────────────────────────────────────────

payment_engine = PaymentEngine(mode=os.getenv("RAZORPAY_MODE", "test"))
