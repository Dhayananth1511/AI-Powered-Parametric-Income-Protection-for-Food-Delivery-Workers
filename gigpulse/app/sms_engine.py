import os
import logging
import httpx
import json

logger = logging.getLogger(__name__)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid_here")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token_here")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

try:
    from twilio.rest import Client
except ModuleNotFoundError:
    Client = None

# Free channel settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY")
CALLMEBOT_W_PHONE = os.getenv("CALLMEBOT_PHONE_NUMBER")

def send_sms_notification(to_phone: str, message: str) -> bool:
    """
    Sends an SMS notification using Twilio.
    Gracefully degrades to logs if credentials are placeholders.
    """
    if not to_phone or not message:
        return False

    is_dummy = ("your_" in TWILIO_ACCOUNT_SID.lower() or "your_" in TWILIO_AUTH_TOKEN.lower())

    if is_dummy:
        logger.info(f"[SIMULATED SMS] To {to_phone}: {message}")
        print(f"[SIMULATED SMS] To {to_phone}: {message}")
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
        logger.error(f"[ERROR] SMS Delivery Failed: {e}")
        print(f"[ERROR] SMS Delivery Failed: {e}")
        return False

def send_whatsapp_notification(to_phone: str, message: str) -> bool:
    """
    Sends a WhatsApp notification using Twilio WhatsApp API.
    To be used by real workers, numbers must be prefixed with '+' (e.g. +919876543210).
    """
    if not to_phone or not message:
        return False

    # Ensure phone number formatting for WhatsApp
    target_phone = to_phone if to_phone.startswith("whatsapp:") else f"whatsapp:{to_phone}"
    
    is_dummy = ("your_" in TWILIO_ACCOUNT_SID.lower() or "your_" in TWILIO_AUTH_TOKEN.lower())

    if is_dummy:
        logger.info(f"[SIMULATED WHATSAPP] To {target_phone}: {message}")
        print(f"[SIMULATED WHATSAPP] To {target_phone}: {message}")
        return True

    try:
        if Client is None:
            raise ModuleNotFoundError("Twilio is not installed")
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        tw_msg = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=target_phone
        )
        logger.info(f"🟢 [REAL WHATSAPP] Sent to {target_phone} - SID: {tw_msg.sid}")
        print(f"🟢 [REAL WHATSAPP] Sent to {target_phone}")
        return True
    except Exception as e:
        logger.error(f"[ERROR] WhatsApp Delivery Failed: {e}")
        print(f"[ERROR] WhatsApp Delivery Failed: {e}")
        return False

def send_telegram_notification(message: str) -> bool:
    """
    Sends a message via Telegram Bot API.
    Professional, free, and instant.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.info(f"[SIMULATED TELEGRAM] {message}")
        print(f"[SIMULATED TELEGRAM] {message}")
        return True

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = httpx.post(url, params=params, timeout=10.0)
        response.raise_for_status()
        logger.info(f"[REAL TELEGRAM] Sent to {TELEGRAM_CHAT_ID}")
        print(f"[REAL TELEGRAM] Sent to {TELEGRAM_CHAT_ID}")
        return True
    except Exception as e:
        logger.error(f"[ERROR] Telegram Delivery Failed: {e}")
        print(f"[ERROR] Telegram Delivery Failed: {e}")
        return False

def send_free_whatsapp_notification(message: str) -> bool:
    """
    Sends a WhatsApp message via CallMeBot API (Free workaround).
    """
    if not CALLMEBOT_API_KEY or not CALLMEBOT_W_PHONE:
        logger.info(f"[SIMULATED FREE WHATSAPP] {message}")
        print(f"[SIMULATED FREE WHATSAPP] {message}")
        return True

    try:
        # Format phone for CallMeBot (should be just numbers with country code)
        phone = CALLMEBOT_W_PHONE.replace("+", "").replace(" ", "").strip()
        url = "https://api.callmebot.com/whatsapp.php"
        params = {
            "phone": phone,
            "text": message,
            "apikey": CALLMEBOT_API_KEY
        }
        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()
        logger.info(f"[REAL FREE WHATSAPP] Sent to {phone}")
        print(f"[REAL FREE WHATSAPP] Sent to {phone}")
        return True
    except Exception as e:
        logger.error(f"[ERROR] CallMeBot Delivery Failed: {e}")
        print(f"[ERROR] CallMeBot Delivery Failed: {e}")
        return False
