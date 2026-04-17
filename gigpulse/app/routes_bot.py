import os
import requests
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/bot", tags=["Assistant Bot"])

class ChatRequest(BaseModel):
    message: str
    worker_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    source: str

# Free HuggingFace Inference API for Zephyr-7b-beta
HF_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
# Read HUGGINGFACE_API_KEY from .env
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

def get_rule_based_fallback(message: str) -> str:
    """A fallback rule-based bot if the HuggingFace API fails or is rate-limited."""
    msg = message.lower()
    if "hello" in msg or "hi" in msg or "hey" in msg:
        return "Hello! I am your GigPulse AI Assistant. How can I help you with your policies, claims, or platform tracking today?"
    elif "login" in msg or "sign in" in msg or "password" in msg:
        return "To log in, click the 'Logout' button if you're already in, or use your email and password at gigpulse_login.html. For workers, use your Swiggy/Zomato email. For admins, use your admin credentials."
    elif "register" in msg or "sign up" in msg or "onboard" in msg:
        return "You can join GigPulse by clicking 'Join as Worker' on the home page or via gigpulse_onboarding.html. You'll need your platform details and basic KYC to get started."
    elif "policy" in msg or "plan" in msg or "renew" in msg:
        return "You can view your active policy, change your plan, or renew it directly from your dashboard's 'Active Policy' section. Let me know if you need help choosing a plan!"
    elif "claim" in msg or "simulate" in msg or "payout" in msg:
        return "Claims on GigPulse are typically processed automatically via our zero-touch pipeline when disruptions occur. You can also simulate a claim using the 'Simulate' button on your dashboard."
    elif "weather" in msg or "aqi" in msg or "curfew" in msg or "disruption" in msg:
        return "GigPulse monitors live data for Rainfall, Temperature, AQI, Cyclones, and Curfews. If a trigger threshold is met in your active zone, you are eligible for a protective payout."
    elif "trust score" in msg:
        return "Your Trust Score determines the speed of your claim approvals. Higher scores mean faster, zero-touch payments. You can maintain a good score by staying active and having successful deliveries."
    else:
        return "I'm your GigPulse tracking assistant. While I couldn't understand that perfectly, I can answer questions about your policies, claims, and disruption triggers. How can I assist you further?"

def query_huggingface(prompt: str) -> Optional[str]:
    headers = {"Content-Type": "application/json"}
    if HF_API_KEY:
        headers["Authorization"] = f"Bearer {HF_API_KEY}"
    
    # Format prompt for zephyr-7b-beta
    formatted_prompt = f"<|system|>\nYou are a helpful and professional customer support assistant for the GigPulse platform. Keep your answers brief and friendly.\n<|user|>\n{prompt}\n<|assistant|>\n"
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.3,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=8)
        if response.status_code != 200:
            logger.error(f"HF API Error {response.status_code}: {response.text}")
            return None
        data = response.json()
        if isinstance(data, list) and len(data) > 0 and 'generated_text' in data[0]:
            return data[0]['generated_text'].strip()
        return None
    except Exception as e:
        logger.error(f"HF Connection Exception: {e}")
        return None

@router.post("/chat", response_model=ChatResponse)
def bot_chat(req: ChatRequest):
    """Chat endpoint using HuggingFace free model API with rule-based fallback."""
    # 1. Try hitting the free HuggingFace LLM
    llm_response = query_huggingface(req.message)
    
    if llm_response:
        return ChatResponse(response=llm_response, source="huggingface")
    
    # 2. Fallback to rule-based logic if LLM fails (e.g., rate limit hit globally)
    fallback_resp = get_rule_based_fallback(req.message)
    return ChatResponse(response=fallback_resp, source="fallback_rules")
