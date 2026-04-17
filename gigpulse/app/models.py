from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON, Index
from sqlalchemy.sql import func
from app.database import Base
import uuid

def gen_id(prefix):
    return prefix + str(uuid.uuid4())[:8].upper()


class Worker(Base):
    __tablename__ = "workers"

    # ── Columns ──────────────────────────────────────────────────────────────
    id               = Column(String, primary_key=True, default=lambda: gen_id("WKR-"))
    name             = Column(String, nullable=False)
    phone            = Column(String, nullable=False, unique=True)
    email            = Column(String, nullable=False, unique=True)
    password         = Column(String, nullable=False)
    platform         = Column(String, nullable=False)
    zone             = Column(String, nullable=False)
    pincode          = Column(String, nullable=False)
    aadhaar_number   = Column(String, nullable=True)
    aadhaar_verified = Column(Boolean, default=False)
    plan             = Column(String, default="standard")
    risk_score       = Column(Float, default=0.5)
    trust_score      = Column(Integer, default=40)
    weekly_hrs_used  = Column(Float, default=0.0)
    payouts          = Column(Float, default=0.0)
    sim_payouts      = Column(Float, default=0.0)
    claims_total     = Column(Integer, default=0)
    claims_approved  = Column(Integer, default=0)
    claims_rejected  = Column(Integer, default=0)
    role             = Column(String, default="worker")
    joined           = Column(DateTime, server_default=func.now())
    plan_effective_date  = Column(DateTime, nullable=True)
    weekly_reset_at      = Column(DateTime, nullable=True)
    is_active            = Column(Boolean, default=True)
    is_online            = Column(Boolean, default=False)
    earnings_protected   = Column(Float, default=0.0)
    bank_upi_id          = Column(String, nullable=True)
    plan_expiry_notified = Column(Boolean, default=False)
    policy_start_date    = Column(DateTime, nullable=True)
    policy_expiry_date   = Column(DateTime, nullable=True)
    policy_status        = Column(String, default="active")
    # policy_status: active | expired | grace_period | pending_renewal

    # ── Indexes — cover all hot-path lookups ──────────────────────────────────
    __table_args__ = (
        Index("ix_workers_email",         "email"),         # login lookup
        Index("ix_workers_phone",         "phone"),         # login / KYC lookup
        Index("ix_workers_zone",          "zone"),          # zone-based filtering
        Index("ix_workers_plan",          "plan"),          # plan distribution queries
        Index("ix_workers_policy_status", "policy_status"), # policy lifecycle queries
        Index("ix_workers_is_active",     "is_active"),     # active worker counts
        Index("ix_workers_aadhaar",       "aadhaar_verified"), # verified counts
        Index("ix_workers_joined",        "joined"),        # new-today queries
    )


class Admin(Base):
    __tablename__ = "admins"

    id          = Column(String, primary_key=True, default=lambda: gen_id("ADM-"))
    name        = Column(String, nullable=False)
    email       = Column(String, nullable=False, unique=True)
    password    = Column(String, nullable=False)
    org         = Column(String, default="ZenVyte GigPulse Platform")
    designation = Column(String, default="Admin")
    phone       = Column(String, nullable=True)
    role        = Column(String, default="admin")
    joined      = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_admins_email", "email"),  # admin login lookup
    )


class Policy(Base):
    __tablename__ = "policies"

    id               = Column(String, primary_key=True, default=lambda: gen_id("POL-"))
    worker_id        = Column(String, nullable=False)
    plan             = Column(String, nullable=False)
    premium          = Column(Float, nullable=False)
    base_premium     = Column(Float, nullable=True)
    risk_adjustment  = Column(Float, nullable=True)
    trust_discount   = Column(Float, nullable=True)
    status           = Column(String, default="active")
    start_date       = Column(DateTime, server_default=func.now())
    end_date         = Column(DateTime, nullable=True)
    effective_date   = Column(DateTime, nullable=True)
    renewal_count    = Column(Integer, default=0)
    created_at       = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_policies_worker_id", "worker_id"),  # per-worker policy history
        Index("ix_policies_status",    "status"),     # active policy filter
    )


class Claim(Base):
    __tablename__ = "claims"

    id                  = Column(String, primary_key=True, default=lambda: gen_id("CLM-"))
    worker_id           = Column(String, nullable=False)
    trigger_type        = Column(String, nullable=False)
    trigger_value       = Column(Float, nullable=True)
    trigger_label       = Column(String, nullable=True)
    disruption_hrs      = Column(Float, default=0.0)
    payout_amount       = Column(Float, default=0.0)
    fraud_score         = Column(Integer, default=0)
    status              = Column(String, default="pending")
    razorpay_order_id   = Column(String, nullable=True)
    razorpay_payment_id = Column(String, nullable=True)
    notes               = Column(Text, nullable=True)
    pipeline_steps      = Column(Text, nullable=True)   # JSON string
    is_simulated        = Column(Boolean, default=False)
    created_at          = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_claims_worker_id",    "worker_id"),   # per-worker claims
        Index("ix_claims_status",       "status"),      # status filter (approved/rejected)
        Index("ix_claims_created_at",   "created_at"),  # time-series trend queries
        Index("ix_claims_trigger_type", "trigger_type"),# trigger analytics
        # Composite: worker + status — used by routes_claims.py heavily
        Index("ix_claims_worker_status", "worker_id", "status"),
    )


class WeatherLog(Base):
    __tablename__ = "weather_logs"

    id          = Column(String, primary_key=True, default=lambda: gen_id("WTH-"))
    zone        = Column(String, nullable=False)
    temperature = Column(Float, nullable=True)
    rainfall    = Column(Float, nullable=True)
    aqi         = Column(Integer, nullable=True)
    wind_speed  = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    alert_type  = Column(String, nullable=True)
    source      = Column(String, default="mock")
    logged_at   = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_weather_zone",       "zone"),      # zone fetch
        Index("ix_weather_logged_at",  "logged_at"), # recent readings
        Index("ix_weather_zone_time",  "zone", "logged_at"),  # composite
    )


class DisruptionEvent(Base):
    """Tracks active disruption monitoring windows per zone."""
    __tablename__ = "disruption_events"

    id               = Column(String, primary_key=True, default=lambda: gen_id("DSR-"))
    zone             = Column(String, nullable=False)
    trigger_type     = Column(String, nullable=False)
    trigger_value    = Column(Float, nullable=True)
    trigger_label    = Column(String, nullable=True)
    status           = Column(String, default="monitoring")
    # status: monitoring | confirming | confirmed | cleared
    confirmation_start = Column(DateTime, nullable=True)
    confirmation_end   = Column(DateTime, nullable=True)
    payout_type      = Column(String, default="hourly")
    disruption_hrs   = Column(Float, default=0.0)
    workers_affected = Column(Integer, default=0)
    created_at       = Column(DateTime, server_default=func.now())
    updated_at       = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_disruption_zone",   "zone"),   # zone-based monitoring
        Index("ix_disruption_status", "status"), # active event filter
    )


class KYCRecord(Base):
    """Simulated Aadhaar KYC verification records."""
    __tablename__ = "kyc_records"

    id             = Column(String, primary_key=True, default=lambda: gen_id("KYC-"))
    worker_id      = Column(String, nullable=False)
    aadhaar_number = Column(String, nullable=False)
    phone          = Column(String, nullable=False)
    otp            = Column(String, nullable=True)
    status         = Column(String, default="pending")
    # status: pending | otp_sent | verified | failed
    attempts       = Column(Integer, default=0)
    verified_at    = Column(DateTime, nullable=True)
    created_at     = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_kyc_worker_id", "worker_id"),      # per-worker KYC lookup
        Index("ix_kyc_aadhaar",   "aadhaar_number"), # duplicate check
    )


class NotificationLog(Base):
    """In-app notifications for workers."""
    __tablename__ = "notifications"

    id          = Column(String, primary_key=True, default=lambda: gen_id("NTF-"))
    worker_id   = Column(String, nullable=False)
    title       = Column(String, nullable=False)
    message     = Column(String, nullable=False)
    notif_type  = Column(String, default="info")
    # type: disruption_alert | payout_credited | plan_change | kyc_done | predictive_alert | info
    is_read     = Column(Boolean, default=False)
    icon        = Column(String, nullable=True)
    amount      = Column(Float, nullable=True)
    created_at  = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_notif_worker_id",      "worker_id"),          # fetch all worker notifs
        Index("ix_notif_is_read",        "is_read"),            # unread count
        Index("ix_notif_worker_unread",  "worker_id", "is_read"), # composite hottest path
    )


class Payment(Base):
    """Payment records tracking Razorpay integration."""
    __tablename__ = "payments"

    id                  = Column(String, primary_key=True, default=lambda: gen_id("PAY-"))
    claim_id            = Column(String, nullable=True)
    worker_id           = Column(String, nullable=False)

    # Razorpay identifiers
    razorpay_order_id   = Column(String, unique=True, nullable=True)
    razorpay_payment_id = Column(String, unique=True, nullable=True)
    signature           = Column(String, nullable=True)

    # Amount (stored in rupees and paise for accuracy)
    amount_rupees       = Column(Float, nullable=False)
    amount_paise        = Column(Integer, nullable=False)

    # State tracking
    status              = Column(String, default="pending")
    # pending → created → confirmed → captured → success / failed → retry
    retry_count         = Column(Integer, default=0)
    max_retries         = Column(Integer, default=3)

    # Error tracking
    error_message       = Column(String(500), nullable=True)
    error_code          = Column(String(50), nullable=True)

    # Timestamps
    created_at          = Column(DateTime, server_default=func.now())
    order_created_at    = Column(DateTime, nullable=True)
    payment_received_at = Column(DateTime, nullable=True)

    # Metadata
    initiated_by        = Column(String(50), default="system")  # system, admin, worker

    __table_args__ = (
        Index("ix_payments_worker_id", "worker_id"),  # per-worker payment history
        Index("ix_payments_claim_id",  "claim_id"),   # claim → payment lookup
        Index("ix_payments_status",    "status"),     # status filter
    )


class PaymentEvent(Base):
    """Audit trail for all payment state changes and webhook events."""
    __tablename__ = "payment_events"

    id              = Column(String, primary_key=True, default=lambda: gen_id("PEV-"))
    payment_id      = Column(String, nullable=False)
    event_type      = Column(String, nullable=False)
    # order_created, webhook_received, capture_initiated, payment_success, payment_failed, retry_initiated
    event_data      = Column(JSON, nullable=True)
    created_at      = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_payment_events_payment_id", "payment_id"),   # audit trail lookup
        Index("ix_payment_events_type",       "event_type"),   # event type filtering
    )