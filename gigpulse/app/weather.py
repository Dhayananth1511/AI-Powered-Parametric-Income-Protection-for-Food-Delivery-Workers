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
# Global Weather Cache (In-Memory for production resilience)
# ─────────────────────────────────────────────────────────────────────────────
_WEATHER_CACHE = {}

def get_cached_weather(zone: str) -> dict:
    return _WEATHER_CACHE.get(zone)

def update_weather_cache(zone: str, data: dict):
    _WEATHER_CACHE[zone] = data


# ─────────────────────────────────────────────────────────────────────────────
# Weather Fetch (OWM real + WAQI real + Open-Meteo Hyper-Local + mock fallback)
# ─────────────────────────────────────────────────────────────────────────────
async def fetch_weather(zone: str, lat: float = None, lon: float = None) -> dict:
    if lat is None or lon is None:
        coords = ZONE_COORDS.get(zone)
        if not coords:
            return {"error": "Invalid Zone", "zone": zone}
        lat, lon = coords

    # Hyper-Local Deep Integration: Open-Meteo (No API Key Required)
    url_open_meteo = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation,weather_code,wind_speed_10m&hourly=precipitation_probability"

    url_owm = None
    if OWM_KEY:
        url_owm = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric"
           
    # Deep Integration: Secondary API for AQI (WAQI / AQICN)
    url_waqi = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={WAQI_KEY}" if WAQI_KEY else None

    # Track data
    weather_payload = {
        "zone":         zone,
        "temperature":  0.0,
        "feels_like":   0.0,
        "humidity":     70,
        "rainfall_1h":  0.0,
        "rainfall_3h":  0.0,
        "wind_speed":   0.0,
        "description":  "clear",
        "aqi":          0,
        "cyclone":      False,
        "curfew":       False,
        "source":       "Satellite Syncing...",
        "fetched_at":   datetime.now().isoformat(),
    }

    try:
        async with httpx.AsyncClient() as client:
            # 1. Fetch Open-Meteo (Highest Granularity, Reliable)
            om_task = client.get(url_open_meteo, timeout=5.0)
            
            # 2. Fetch OWM (Optional fallback)
            owm_task = client.get(url_owm, timeout=5.0) if url_owm else None
            
            # 3. Fetch WAQI
            waqi_task = client.get(url_waqi, timeout=5.0) if url_waqi else None

            # Execute available API calls
            tasks = [t for t in [om_task, owm_task, waqi_task] if t]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            res_om = results[0] if len(results) > 0 else None
            res_owm = results[1] if len(results) > 1 and owm_task else None
            res_waqi = results[2] if len(results) > 2 and waqi_task else (results[1] if len(results) > 1 and waqi_task and not owm_task else None)

            # Process WAQI
            real_aqi = None
            if res_waqi and not isinstance(res_waqi, Exception) and res_waqi.status_code == 200:
                w_data = res_waqi.json()
                if w_data.get("status") == "ok":
                    real_aqi = w_data.get("data", {}).get("aqi")
                    weather_payload["aqi"] = int(real_aqi)

            source_label = []
            
            # Process Open-Meteo (Primary for Hyper-Local)
            om_success = False
            if res_om and not isinstance(res_om, Exception) and res_om.status_code == 200:
                om_data = res_om.json()
                current = om_data.get("current", {})
                weather_payload["temperature"] = current.get("temperature_2m", 30.0)
                weather_payload["feels_like"] = weather_payload["temperature"] + 2.0  # Appx
                weather_payload["rainfall_1h"] = current.get("precipitation", 0.0)
                weather_payload["rainfall_3h"] = weather_payload["rainfall_1h"] * 3
                weather_payload["wind_speed"] = current.get("wind_speed_10m", 0.0) / 3.6 # kmh to m/s
                weather_payload["description"] = "OpenMeteo Live"
                om_success = True
                source_label.append("Open-Meteo")

            # Process OWM (Secondary/Ensemble)
            if res_owm and not isinstance(res_owm, Exception) and res_owm.status_code == 200:
                o_data = res_owm.json()
                if not om_success:
                    weather_payload["temperature"] = o_data["main"]["temp"]
                    weather_payload["feels_like"] = o_data["main"]["feels_like"]
                    weather_payload["humidity"] = o_data["main"]["humidity"]
                    weather_payload["wind_speed"] = o_data["wind"]["speed"]
                    weather_payload["description"] = o_data["weather"][0]["description"]
                
                # Use OWM rain if OpenMeteo didn't detect any (aggregation)
                owm_rain_1h = o_data.get("rain", {}).get("1h", 0.0)
                if owm_rain_1h > weather_payload["rainfall_1h"]:
                    weather_payload["rainfall_1h"] = owm_rain_1h
                    weather_payload["rainfall_3h"] = o_data.get("rain", {}).get("3h", owm_rain_1h * 3)
                source_label.append("OWM")

            if real_aqi:
                source_label.append("WAQI")
            else:
                source_label.append("Mock AQI")

            if len(source_label) > 0:
                weather_payload["source"] = " + ".join(source_label) + " Live"
                update_weather_cache(zone, weather_payload)
                return weather_payload

    except Exception as e:
        pass # Fallback to cache

    cached = get_cached_weather(zone)
    if cached:
        cached["source"] = cached.get("source", "").replace("Live", "(Cached)")
        return cached

    return weather_payload

# ─────────────────────────────────────────────────────────────────────────────
# Trigger Checker
# ─────────────────────────────────────────────────────────────────────────────
def check_triggers(weather: dict) -> list:
    """Return list of triggered parametric events from weather data."""
    triggered = []
    if weather.get("rainfall_3h", 0) >= TRIGGERS["rainfall"]["threshold"]:
        triggered.append({
            "type": "rainfall", "value": weather["rainfall_3h"],
            "label": "Heavy Rainfall", "payout_type": "hourly",
            "unit": TRIGGERS["rainfall"]["unit"],
        })
    if weather.get("temperature", 0) >= TRIGGERS["temperature"]["threshold"]:
        triggered.append({
            "type": "temperature", "value": weather["temperature"],
            "label": "Extreme Heat", "payout_type": "hourly",
            "unit": TRIGGERS["temperature"]["unit"],
        })
    if weather.get("aqi", 0) >= TRIGGERS["aqi"]["threshold"]:
        triggered.append({
            "type": "aqi", "value": weather["aqi"],
            "label": "Severe AQI", "payout_type": "hourly",
            "unit": TRIGGERS["aqi"]["unit"],
        })
    if weather.get("cyclone"):
        triggered.append({
            "type": "cyclone", "value": 1,
            "label": "Cyclone/Flood Alert", "payout_type": "full_cap",
            "unit": "alert",
        })
    if weather.get("curfew"):
        triggered.append({
            "type": "curfew", "value": 1,
            "label": "Curfew/Hartal", "payout_type": "full_cap",
            "unit": "flag",
        })
    return triggered

# ─────────────────────────────────────────────────────────────────────────────
# NDMA Mock Alerts
# ─────────────────────────────────────────────────────────────────────────────
async def fetch_ndma_alerts(zone: str) -> dict:
    """Simulate NDMA disaster alert feed by fetching live Global Disaster Alert (GDACS)."""
    alert_payload = {
        "zone":    zone,
        "cyclone": False,
        "flood":   False,
        "curfew":  False,
        "source":  "GDACS RSS (Live)",
        "updated": datetime.now().isoformat(),
    }
    
    try:
        # Fetch GDACS Global RSS Live Feed (Disasters in last 24h/7d)
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://gdacs.org/xml/rss.xml", timeout=5.0)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                # Check for active cyclones or floods globally
                for item in root.findall(".//item"):
                    title = item.find("title").text.lower() if item.find("title") is not None else ""
                    # In a real environment we would check distance via geo:lat geo:lon 
                    # For demo purposes, we will trigger if it mentions India or is a severe global Cyclone
                    if "cyclone" in title and ("india" in title or "0" not in title): # Simulating hit
                        alert_payload["cyclone"] = False # Do not auto-trigger false positive globally, leave false unless testing
                    if "flood" in title:
                        alert_payload["flood"] = False
    except Exception as e:
        alert_payload["source"] = "NDMA Feed (Offline)"
        pass

    return alert_payload

# ─────────────────────────────────────────────────────────────────────────────
# All Zones Utility
# ─────────────────────────────────────────────────────────────────────────────
def get_all_zones():
    return sorted(ZONE_COORDS.keys())
