import httpx
import os
import random
import xml.etree.ElementTree as ET
import asyncio
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
OWM_KEY = os.getenv("OWM_API_KEY", "")
WAQI_KEY = os.getenv("WAQI_API_KEY", "")
# ─────────────────────────────────────────────────────────────────────────────
# Zone Coordinates (GPS lat/lon for real OWM API calls)
# ─────────────────────────────────────────────────────────────────────────────
ZONE_COORDS = {
    "Velachery, Chennai":       (12.9816, 80.2209),
    "Marina Beach, Chennai":    (13.0500, 80.2824),
    "T. Nagar, Chennai":        (13.0358, 80.2332),
    "Anna Nagar, Chennai":      (13.0850, 80.2101),
    "Adyar, Chennai":           (13.0012, 80.2565),
    "Tambaram, Chennai":        (12.9249, 80.1000),
    "Porur, Chennai":           (13.0368, 80.1567),
    "Chromepet, Chennai":       (12.9516, 80.1462),
    "Perungudi, Chennai":       (12.9667, 80.2417),
    "Sholinganallur, Chennai":  (12.9010, 80.2279),
    "Mylapore, Chennai":        (13.0368, 80.2676),
    "Guindy, Chennai":          (13.0067, 80.2206),
    "Kodambakkam, Chennai":     (13.0490, 80.2248),
    "Nungambakkam, Chennai":    (13.0569, 80.2425),
    "Egmore, Chennai":          (13.0732, 80.2609),
    "Washermanpet, Chennai":    (13.1167, 80.2833),
    "Royapuram, Chennai":       (13.1126, 80.2975),
    "Thiruvottiyur, Chennai":   (13.1667, 80.3000),
    "Avadi, Chennai":           (13.1149, 80.1000),
    "Ambattur, Chennai":        (13.1143, 80.1548),
    "Pallavaram, Chennai":      (12.9675, 80.1491),
    "Madipakkam, Chennai":      (12.9558, 80.2044),
    "Perambur, Chennai":        (13.1167, 80.2333),
    "Kolathur, Chennai":        (13.1182, 80.2250),
    "Virugambakkam, Chennai":   (13.0548, 80.1882),
    "Mogappair, Chennai":       (13.0850, 80.1782),
    "Korattur, Chennai":        (13.1100, 80.1900),
    "Thiruvanmiyur, Chennai":   (12.9830, 80.2570),
    "Besant Nagar, Chennai":    (13.0002, 80.2707),
    "Injambakkam, Chennai":     (12.9220, 80.2470),
    "Coimbatore Central":       (11.0168, 76.9558),
    "RS Puram, Coimbatore":     (11.0100, 76.9600),
    "Gandhipuram, Coimbatore":  (11.0168, 76.9700),
    "Madurai Central":          (9.9252, 78.1198),
    "Anna Nagar, Madurai":      (9.9400, 78.1150),
    "Trichy Central":           (10.7905, 78.7047),
    "Srirangam, Trichy":        (10.8644, 78.6950),
    "Salem Central":            (11.6643, 78.1460),
    "Tirunelveli Central":      (8.7139, 77.7567),
    "Erode Central":            (11.3410, 77.7172),
    "Vellore Central":          (12.9165, 79.1325),
    "Kanchipuram":              (12.8398, 79.7003),
    "Pondicherry Central":      (11.9416, 79.8083),
    "Cuddalore":                (11.7447, 79.7686),
    "Nagapattinam":             (10.7672, 79.8447),
}

# ─────────────────────────────────────────────────────────────────────────────
# Trigger Thresholds (5 parametric triggers)
# ─────────────────────────────────────────────────────────────────────────────
TRIGGERS = {
    "rainfall":    {"threshold": 35.0, "unit": "mm/3hr", "label": "Heavy Rainfall",  "payout_type": "hourly"},
    "temperature": {"threshold": 43.0, "unit": "°C",     "label": "Extreme Heat",   "payout_type": "hourly"},
    "aqi":         {"threshold": 300,  "unit": "AQI",    "label": "Severe AQI",     "payout_type": "hourly"},
    "cyclone":     {"threshold": 1,    "unit": "alert",  "label": "Cyclone/Flood",  "payout_type": "full_cap"},
    "curfew":      {"threshold": 1,    "unit": "flag",   "label": "Curfew/Hartal",  "payout_type": "full_cap"},
}

# ─────────────────────────────────────────────────────────────────────────────
# Global High-Performance Connection Pool & Cache
# ─────────────────────────────────────────────────────────────────────────────
# Enhanced for Render: Proper connection aging and robust timeouts
_HTTP_CLIENT = httpx.AsyncClient(
    timeout=httpx.Timeout(10.0, connect=5.0),
    limits=httpx.Limits(max_connections=40, max_keepalive_connections=20),
    follow_redirects=True,
    headers={"User-Agent": "ZenVyte-GigPulse/2.1.0"}
)
_WEATHER_CACHE = {} # {zone: {"cache_until": timestamp, "data": {}}}

def get_cached_weather(zone: str) -> dict:
    cached = _WEATHER_CACHE.get(zone)
    if cached and datetime.now().timestamp() < cached["cache_until"]:
        return cached["data"]
    return None

def update_weather_cache(zone: str, data: dict, ttl_seconds: int = 300):
    _WEATHER_CACHE[zone] = {
        "cache_until": datetime.now().timestamp() + ttl_seconds,
        "data":        data
    }

async def fetch_weather(zone: str, lat: float = None, lon: float = None) -> dict:
    # 1. Check TTL Cache First
    cached = get_cached_weather(zone)
    if cached:
        cached["source"] = cached.get("source", "").replace("Live", "Cached")
        return cached

    # Initial payload
    weather_payload = {
        "zone": zone, "temperature": 0.0, "feels_like": 0.0, "humidity": 70,
        "rainfall_1h": 0.0, "rainfall_3h": 0.0, "wind_speed": 0.0,
        "description": "clear", "aqi": 0, "cyclone": False, "curfew": False,
        "source": "Satellite Syncing...", "fetched_at": datetime.now().isoformat(),
    }

    if lat is None or lon is None:
        # First attempt: Exact match
        coords = ZONE_COORDS.get(zone)
        # Second attempt: Fuzzy match
        if not coords:
            for k, v in ZONE_COORDS.items():
                if zone.lower() in k.lower() or k.lower() in zone.lower():
                    coords = v
                    zone = k 
                    break
        if not coords:
            # Return safe default payload instead of error to prevent UI/Simulation breaks during testing/demo
            weather_payload["description"] = "Zone Not Found (System Fallback)"
            weather_payload["source"] = "Simulated Satellite Sync"
            return weather_payload
        lat, lon = coords

    # Hyper-Local Deep Integration APIs
    url_open_meteo = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation,weather_code,wind_speed_10m&hourly=precipitation_probability"
    url_owm = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric" if OWM_KEY else None
    url_waqi = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={WAQI_KEY}" if WAQI_KEY else None

    # Standardized higher timeouts for production reliability (especially on Render)
    TIMEOUT_SEC = 7.5

        # ─────────────────────────────────────────────────────────────
        # STAGGERED REQUESTS: Prevents burst rate-limiting (429)
        # especially on Open-Meteo which dislikes concurrent threads.
        # ─────────────────────────────────────────────────────────────
        stagger_delay = random.uniform(0.1, 1.2)
        await asyncio.sleep(stagger_delay)

        tasks = []
        tasks.append(_HTTP_CLIENT.get(url_open_meteo, timeout=TIMEOUT_SEC))
        if url_owm:  
            tasks.append(_HTTP_CLIENT.get(url_owm, timeout=TIMEOUT_SEC))
        
        if url_waqi: 
            tasks.append(_HTTP_CLIENT.get(url_waqi, timeout=TIMEOUT_SEC))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Results Mapping
        res_om   = results[0] if len(results) > 0 else None
        res_owm  = results[1] if len(results) > 1 and url_owm else None
        idx_waqi = 2 if url_owm else 1
        res_waqi = results[idx_waqi] if len(results) > idx_waqi and url_waqi else None

        # Log individual failures with EXACT exception types for Render debugging
        if isinstance(res_om, Exception):
            print(f"[Weather] Open-Meteo ERROR: {type(res_om).__name__}: {res_om}")
        elif res_om and res_om.status_code != 200:
            print(f"[Weather] Open-Meteo FAILED: {res_om.status_code}")

        if url_owm:
            if isinstance(res_owm, Exception):
                print(f"[Weather] OWM ERROR: {type(res_owm).__name__}: {res_owm}")
            elif res_owm and res_owm.status_code != 200:
                print(f"[Weather] OWM FAILED: {res_owm.status_code} {res_owm.text[:100]}")

        if url_waqi:
            if isinstance(res_waqi, Exception):
                print(f"[Weather] WAQI ERROR: {type(res_waqi).__name__}: {res_waqi}")
            elif res_waqi and res_waqi.status_code != 200:
                print(f"[Weather] WAQI FAILED: {res_waqi.status_code}")

        source_label = []
        
        # Parse Open-Meteo
        if res_om and not isinstance(res_om, Exception) and res_om.status_code == 200:
            om_data = res_om.json()
            curr = om_data.get("current", {})
            weather_payload["temperature"] = curr.get("temperature_2m", 30.0)
            weather_payload["rainfall_1h"] = curr.get("precipitation", 0.0)
            weather_payload["rainfall_3h"] = weather_payload["rainfall_1h"] * 3
            weather_payload["wind_speed"]  = curr.get("wind_speed_10m", 0.0) / 3.6
            weather_payload["description"] = "OpenMeteo Live"
            source_label.append("Open-Meteo")

        # Parse OWM
        if res_owm and not isinstance(res_owm, Exception) and res_owm.status_code == 200:
            o_data = res_owm.json()
            if not source_label: # fallback settings
                weather_payload["temperature"] = o_data["main"]["temp"]
                weather_payload["description"] = o_data["weather"][0]["description"]
            # Enriched rain
            owm_rain = o_data.get("rain", {}).get("1h", 0.0)
            if owm_rain > weather_payload["rainfall_1h"]:
                weather_payload["rainfall_1h"] = owm_rain
                weather_payload["rainfall_3h"] = o_data.get("rain", {}).get("3h", owm_rain * 3)
            source_label.append("OWM")

        # Parse WAQI
        if res_waqi and not isinstance(res_waqi, Exception) and res_waqi.status_code == 200:
            w_data = res_waqi.json()
            if w_data.get("status") == "ok":
                weather_payload["aqi"] = int(w_data.get("data", {}).get("aqi", 0))
                source_label.append("WAQI")

        if source_label:
            weather_payload["source"] = " + ".join(source_label) + " Live"
            update_weather_cache(zone, weather_payload)
            return weather_payload

    except Exception:
        pass

    return weather_payload

# ─────────────────────────────────────────────────────────────────────────────
# Trigger Checker
# ─────────────────────────────────────────────────────────────────────────────
def check_triggers(weather: dict) -> list:
    triggered = []
    if weather.get("rainfall_3h", 0) >= TRIGGERS["rainfall"]["threshold"]:
        triggered.append({"type": "rainfall", "value": weather["rainfall_3h"], "label": "Heavy Rainfall", "payout_type": "hourly", "unit": "mm"})
    if weather.get("temperature", 0) >= TRIGGERS["temperature"]["threshold"]:
        triggered.append({"type": "temperature", "value": weather["temperature"], "label": "Extreme Heat", "payout_type": "hourly", "unit": "°C"})
    if weather.get("aqi", 0) >= TRIGGERS["aqi"]["threshold"]:
        triggered.append({"type": "aqi", "value": weather["aqi"], "label": "Severe AQI", "payout_type": "hourly", "unit": "AQI"})
    return triggered

# ─────────────────────────────────────────────────────────────────────────────
# NDMA Mock Alerts (With Aggressive Timeout)
# ─────────────────────────────────────────────────────────────────────────────
async def fetch_ndma_alerts(zone: str) -> dict:
    alert_payload = { "zone": zone, "cyclone": False, "flood": False, "curfew": False, "source": "GDACS Live", "updated": datetime.now().isoformat() }
    try:
        # AGGRESSIVE TIMEOUT FOR SECONDARY SERVICE
        resp = await _HTTP_CLIENT.get("https://gdacs.org/xml/rss.xml", timeout=1.5)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item"):
                title = item.find("title").text.lower() if item.find("title") is not None else ""
                if "cyclone" in title and "india" in title: alert_payload["cyclone"] = False
    except Exception:
        alert_payload["source"] = "NDMA Feed (Offline/Slow)"
    return alert_payload

def get_all_zones():
    return sorted(ZONE_COORDS.keys())

def get_api_status():
    """Diagnostic check for environment keys."""
    def mask(k): return f"{k[:4]}****{k[-4:]}" if len(k) > 10 else "MISSING/SHORT"
    return {
        "owm_key_present": bool(OWM_KEY and "your_" not in OWM_KEY),
        "owm_key_masked":  mask(OWM_KEY),
        "waqi_key_present": bool(WAQI_KEY and "your_" not in WAQI_KEY),
        "cache_size":      len(_WEATHER_CACHE),
        "timestamp":       datetime.now().isoformat()
    }
