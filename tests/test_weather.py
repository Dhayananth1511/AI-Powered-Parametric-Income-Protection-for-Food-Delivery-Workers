import pytest
import asyncio
from app.weather import fetch_weather

@pytest.mark.asyncio
async def test_fetch_weather_fallback():
    # Calling this without an API key should safely fallback to the mock generator
    weather = await fetch_weather("Unknown Zone")
    
    assert weather is not None
    assert "temperature" in weather
    assert "rainfall_1h" in weather
    assert "aqi" in weather
    assert weather["zone"] == "Unknown Zone"

@pytest.mark.asyncio
async def test_fetch_weather_known_zone():
    # Testing known zone fallback
    weather = await fetch_weather("Velachery, Chennai")
    assert weather is not None
    assert weather["zone"] == "Velachery, Chennai"
    assert isinstance(weather["aqi"], int)
