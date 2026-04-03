"""
Notification Routes — In-app notification system (FCM-style)
Endpoints: GET/POST /notifications/*
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import NotificationLog
from datetime import datetime
import uuid

router = APIRouter(prefix="/notifications", tags=["notifications"])

NOTIF_ICONS = {
    "disruption_alert":  "🌧️",
    "payout_credited":   "💰",
    "plan_change":       "📋",
    "kyc_done":          "✅",
    "predictive_alert":  "⚡",
    "info":              "ℹ️",
}

class SendNotif(BaseModel):
    worker_id:  str
    title:      str
    message:    str
    notif_type: str = "info"
    amount:     float = None
    icon:       str = None

class MarkRead(BaseModel):
    notif_ids:  list = []
    worker_id:  str = None  # if set, mark ALL for worker as read

# ─────────────────────────────────────────────────────────────────────────────
# GET all notifications for a worker
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/{worker_id}")
def get_notifications(worker_id: str, limit: int = 30, db: Session = Depends(get_db)):
    notifs = (db.query(NotificationLog)
              .filter(NotificationLog.worker_id == worker_id)
              .order_by(NotificationLog.created_at.desc())
              .limit(limit)
              .all())
    unread_count = sum(1 for n in notifs if not n.is_read)
    return {
        "worker_id":    worker_id,
        "unread_count": unread_count,
        "notifications": [
            {
                "id":         n.id,
                "title":      n.title,
                "message":    n.message,
                "notif_type": n.notif_type,
                "icon":       n.icon or NOTIF_ICONS.get(n.notif_type, "ℹ️"),
                "is_read":    n.is_read,
                "amount":     n.amount,
                "created_at": str(n.created_at),
                "time_ago":   _time_ago(n.created_at),
            }
            for n in notifs
        ]
    }

# ─────────────────────────────────────────────────────────────────────────────
# POST mark notifications as read
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/mark-read")
def mark_read(req: MarkRead, db: Session = Depends(get_db)):
    if req.worker_id:
        db.query(NotificationLog).filter(
            NotificationLog.worker_id == req.worker_id,
            NotificationLog.is_read   == False
        ).update({"is_read": True})
    elif req.notif_ids:
        db.query(NotificationLog).filter(
            NotificationLog.id.in_(req.notif_ids)
        ).update({"is_read": True}, synchronize_session=False)
    db.commit()
    return {"success": True, "message": "Notifications marked as read"}

# ─────────────────────────────────────────────────────────────────────────────
# POST send notification (internal use)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/send")
def send_notification(req: SendNotif, db: Session = Depends(get_db)):
    notif = NotificationLog(
        worker_id  = req.worker_id,
        title      = req.title,
        message    = req.message,
        notif_type = req.notif_type,
        amount     = req.amount,
        icon       = req.icon or NOTIF_ICONS.get(req.notif_type, "ℹ️"),
    )
    db.add(notif)
    db.commit()
    return {"success": True, "notif_id": notif.id}

# ─────────────────────────────────────────────────────────────────────────────
# GET unread count only (for polling badge)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/unread/{worker_id}")
def unread_count(worker_id: str, db: Session = Depends(get_db)):
    count = db.query(NotificationLog).filter(
        NotificationLog.worker_id == worker_id,
        NotificationLog.is_read   == False
    ).count()
    return {"worker_id": worker_id, "unread_count": count}

# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────
def _time_ago(dt: datetime) -> str:
    if not dt:
        return ""
    now = datetime.now()
    diff = (now - dt).total_seconds()
    if diff < 60:    return "just now"
    if diff < 3600:  return f"{int(diff/60)}m ago"
    if diff < 86400: return f"{int(diff/3600)}h ago"
    return f"{int(diff/86400)}d ago"
