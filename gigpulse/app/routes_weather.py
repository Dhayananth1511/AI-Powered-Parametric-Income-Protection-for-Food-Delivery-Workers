from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import WeatherLog
from app.weather import fetch_weather, check_triggers, fetch_ndma_alerts
from app.trigger_monitor import get_zone_status
from datetime import datetime

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/zone/{zone}")
async def get_weather(zone: str, db: Session = Depends(get_db)):
    weather  = await fetch_weather(zone)
    triggers = check_triggers(weather)
    ndma     = fetch_ndma_alerts(zone)
    zone_st  = get_zone_status(zone)

    # Log to DB
    log = WeatherLog(
        zone        = zone,
        temperature = weather.get("temperature"),
        rainfall    = weather.get("rainfall_3h", 0),
        aqi         = weather.get("aqi"),
        wind_speed  = weather.get("wind_speed"),
        description = weather.get("description"),
        alert_type  = triggers[0]["type"] if triggers else None,
        source      = weather.get("source", "unknown"),
    )
    db.add(log)
    db.commit()

    return {
        "zone":         zone,
        "weather":      weather,
        "triggers":     triggers,
        "ndma":         ndma,
        "zone_status":  zone_st,
        "has_trigger":  len(triggers) > 0,
        "trigger_count":len(triggers),
        "fetched_at":   datetime.now().isoformat(),
    }

@router.get("/live-demo/{zone}")
async def live_demo_weather(zone: str):
    import httpx
    import os
    from fastapi import HTTPException
    
    OWM_KEY = os.getenv("OWM_API_KEY", "")
    if not OWM_KEY or OWM_KEY == "your_owm_key_here":
        raise HTTPException(status_code=500, detail="Missing valid OWM_API_KEY in .env")
        
    from app.weather import ZONE_COORDS
    coords = ZONE_COORDS.get(zone, (13.0827, 80.2707))
    lat, lon = coords
    
    url = (f"https://api.openweathermap.org/data/2.5/weather"
           f"?lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric")
           
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=8.0)
        return {"live_raw_response": resp.json(), "http_status": resp.status_code, "request_url": url.replace(OWM_KEY, "HIDDEN_KEY")}

@router.get("/all-zones")
async def get_all_zone_weather():
    from app.weather import ZONE_COORDS
    from app.ml_engine import ZONE_DATA
    zones_summary = []
    for zone in list(ZONE_COORDS.keys())[:10]:  # Top 10 for performance
        w = await fetch_weather(zone)
        t = check_triggers(w)
        zones_summary.append({
            "zone":    zone,
            "temp":    w.get("temperature"),
            "rain":    w.get("rainfall_3h", 0),
            "aqi":     w.get("aqi"),
            "status":  "⚡ ALERT" if t else "✅ Clear",
            "triggers":t,
        })
    return {"zones": zones_summary, "fetched_at": datetime.now().isoformat()}

@router.get("/logs")
def get_weather_logs(limit: int = 20, db: Session = Depends(get_db)):
    logs = db.query(WeatherLog).order_by(WeatherLog.logged_at.desc()).limit(limit).all()
    return [
        {
            "id": l.id, "zone": l.zone, "temperature": l.temperature,
            "rainfall": l.rainfall, "aqi": l.aqi, "alert_type": l.alert_type,
            "source": l.source, "logged_at": str(l.logged_at),
        }
        for l in logs
    ]