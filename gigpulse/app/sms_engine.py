import os
import logging

logger = logging.getLogger(__name__)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid_here")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token_here")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")

try:
    from twilio.rest import Client
except ModuleNotFoundError:
    Client = None

def send_sms_notification(to_phone: str, message: str) -> bool:
    """
    Sends an SMS notification using Twilio.
    Gracefully degrades to logs if credentials are placeholders.
    """
    if not to_phone or not message:
        return False

    is_dummy = ("your_" in TWILIO_ACCOUNT_SID.lower() or "your_" in TWILIO_AUTH_TOKEN.lower())

    if is_dummy:
        logger.info(f"📱 [SIMULATED SMS] To {to_phone}: {message}")
        print(f"📱 [SIMULATED SMS] To {to_phone}: {message}")
        return True

    try:
        if Client is None:
            raise ModuleNotFoundError("Twilio is not installed")
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        tw_msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        logger.info(f"📱 [REAL SMS] Sent to {to_phone} - SID: {tw_msg.sid}")
        print(f"📱 [REAL SMS] Sent to {to_phone}")
        return True
    except Exception as e:
        logger.error(f"❌ SMS Delivery Failed: {e}")
        print(f"❌ SMS Delivery Failed: {e}")
        return False
