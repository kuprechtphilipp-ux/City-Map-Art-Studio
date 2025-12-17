"""
osm.py

Fetches geometric map data from OpenStreetMap
using the Overpass API.
"""

import requests
import time

URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

HEADERS = {"User-Agent": "CityMapArt/1.0"}

def fetch_osm(lat, lon, radius):
    time.sleep(1)

    query = f"""
    [out:json][timeout:25];
    (
      way["building"](around:{radius},{lat},{lon});
      way["natural"="water"](around:{radius},{lat},{lon});
      way["leisure"="park"](around:{radius},{lat},{lon});
      way["landuse"="grass"](around:{radius},{lat},{lon});
      way["highway"](around:{radius},{lat},{lon});
    );
    out geom;
    """

    data = None
    for url in URLS:
        try:
            r = requests.post(url, data=query, headers=HEADERS, timeout=30)
            r.raise_for_status()
            data = r.json()
            break
        except Exception:
            pass

    if not data:
        return {k: [] for k in ["building", "water", "green", "road"]}

    out = {"building": [], "water": [], "green": [], "road": []}

    for el in data.get("elements", []):
        if el["type"] != "way":
            continue

        coords = [[p["lon"], p["lat"]] for p in el["geometry"]]
        tags = el.get("tags", {})

        if "building" in tags:
            out["building"].append({"path": coords})
        elif tags.get("natural") == "water":
            out["water"].append({"path": coords})
        elif tags.get("leisure") == "park" or tags.get("landuse") == "grass":
            out["green"].append({"path": coords})
        elif "highway" in tags:
            out["road"].append({"path": coords})

    return out
