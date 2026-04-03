import httpx
import os
import random
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
OWM_KEY = os.getenv("OWM_API_KEY", "")

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
# Mock AQI per zone (CPCB simulation)
# ─────────────────────────────────────────────────────────────────────────────
ZONE_AQI = {
    "Velachery, Chennai": 142,    "Marina Beach, Chennai": 89,
    "T. Nagar, Chennai": 178,     "Anna Nagar, Chennai": 95,
    "Adyar, Chennai": 134,        "Tambaram, Chennai": 112,
    "Guindy, Chennai": 198,       "Porur, Chennai": 145,
    "Chromepet, Chennai": 132,    "Perungudi, Chennai": 158,
    "Sholinganallur, Chennai": 121,"Mylapore, Chennai": 162,
    "Kodambakkam, Chennai": 138,  "Nungambakkam, Chennai": 105,
    "Egmore, Chennai": 148,       "Washermanpet, Chennai": 175,
    "Royapuram, Chennai": 168,    "Thiruvottiyur, Chennai": 182,
    "Ambattur, Chennai": 155,     "Avadi, Chennai": 118,
    "Pallavaram, Chennai": 115,   "Madipakkam, Chennai": 145,
    "Perambur, Chennai": 162,     "Kolathur, Chennai": 135,
    "Mogappair, Chennai": 102,    "Korattur, Chennai": 142,
    "Thiruvanmiyur, Chennai": 128,"Besant Nagar, Chennai": 88,
    "Injambakkam, Chennai": 92,   "Virugambakkam, Chennai": 138,
    "Coimbatore Central": 95,     "RS Puram, Coimbatore": 88,
    "Gandhipuram, Coimbatore": 105,"Madurai Central": 135,
    "Anna Nagar, Madurai": 118,   "Trichy Central": 125,
    "Srirangam, Trichy": 108,     "Salem Central": 115,
    "Tirunelveli Central": 98,    "Erode Central": 112,
    "Vellore Central": 125,       "Kanchipuram": 118,
    "Pondicherry Central": 92,    "Cuddalore": 105,
    "Nagapattinam": 88,
}

def _mock_aqi(zone: str) -> int:
    base = ZONE_AQI.get(zone, 120)
    variation = random.randint(-15, 25)
    return max(0, base + variation)

def _mock_weather(zone: str) -> dict:
    """Realistic fallback mock weather with variation."""
    hour = datetime.now().hour
    # Evening (6–10pm) has higher rainfall simulation
    base_rain = 0.0
    if 18 <= hour <= 22:
        base_rain = round(random.uniform(0, 8), 2)

    return {
        "zone":         zone,
        "temperature":  round(random.uniform(30, 37), 1),
        "feels_like":   round(random.uniform(34, 42), 1),
        "humidity":     random.randint(65, 88),
        "rainfall_1h":  base_rain,
        "rainfall_3h":  round(base_rain * random.uniform(2.5, 3.5), 2),
        "wind_speed":   round(random.uniform(8, 22), 1),
        "description":  random.choice(["partly cloudy", "overcast clouds", "light rain", "scattered clouds"]),
        "aqi":          _mock_aqi(zone),
        "cyclone":      False,
        "curfew":       False,
        "source":       "Mock (OWM fallback)",
        "fetched_at":   datetime.now().isoformat(),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Weather Fetch (OWM real + mock fallback)
# ─────────────────────────────────────────────────────────────────────────────
async def fetch_weather(zone: str) -> dict:
    coords = ZONE_COORDS.get(zone)
    if not coords or not OWM_KEY:
        return _mock_weather(zone)
    lat, lon = coords
    url = (f"https://api.openweathermap.org/data/2.5/weather"
           f"?lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=8.0)
            if resp.status_code == 200:
                data = resp.json()
                rainfall_1h = data.get("rain", {}).get("1h", 0.0)
                rainfall_3h = data.get("rain", {}).get("3h", rainfall_1h * 3)
                return {
                    "zone":         zone,
                    "temperature":  data["main"]["temp"],
                    "feels_like":   data["main"]["feels_like"],
                    "humidity":     data["main"]["humidity"],
                    "rainfall_1h":  rainfall_1h,
                    "rainfall_3h":  rainfall_3h,
                    "wind_speed":   data["wind"]["speed"],
                    "description":  data["weather"][0]["description"],
                    "aqi":          _mock_aqi(zone),
                    "cyclone":      False,
                    "curfew":       False,
                    "source":       "OpenWeatherMap Live",
                    "fetched_at":   datetime.now().isoformat(),
                }
    except Exception as e:
        print(f"[OWM] Fetch error for {zone}: {e}")
    return _mock_weather(zone)

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
def fetch_ndma_alerts(zone: str) -> dict:
    """Simulate NDMA disaster alert feed."""
    return {
        "zone":    zone,
        "cyclone": False,
        "flood":   False,
        "curfew":  False,
        "source":  "NDMA Mock Feed",
        "updated": datetime.now().isoformat(),
    }

# ─────────────────────────────────────────────────────────────────────────────
# All Zones Utility
# ─────────────────────────────────────────────────────────────────────────────
def get_all_zones():
    return sorted(ZONE_COORDS.keys())