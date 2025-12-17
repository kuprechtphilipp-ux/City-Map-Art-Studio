"""
geocoding.py

Uses the Nominatim API to convert a city name
into latitude, longitude and a display name.
"""

import requests
import time

URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "CityMapArt/1.0"}

def geocode_city(city):
    time.sleep(1)  # be polite to the API
    r = requests.get(
        URL,
        params={"q": city, "format": "json", "limit": 1},
        headers=HEADERS,
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    if not data:
        raise ValueError("City not found")
    return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
