import requests
import time

URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

HEADERS = {"User-Agent": "CityMapArt/1.0"}

def fetch_pois(lat, lon, radius, limit=100):
    time.sleep(1)

    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"="attraction"](around:{radius},{lat},{lon});
      node["historic"](around:{radius},{lat},{lon});
      node["amenity"="restaurant"](around:{radius},{lat},{lon});
      node["tourism"="museum"](around:{radius},{lat},{lon});
      node["leisure"="park"](around:{radius},{lat},{lon});
    );
    out;
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
        return []

    pois = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name")
        if not name:
            continue

        if tags.get("tourism") == "museum":
            category = "Museum"
        elif tags.get("amenity") == "restaurant":
            category = "Restaurant"
        elif tags.get("leisure") == "park":
            category = "Nature"
        elif tags.get("historic"):
            category = "Historic"
        else:
            category = "Attraction"

        pois.append(
            {
                "name": name,
                "lat": el["lat"],
                "lon": el["lon"],
                "category": category,
            }
        )

    return pois[:limit]
