import streamlit as st
import copy
import math
import pandas as pd

from services.geocoding import geocode_city
from services.osm import fetch_osm
from services.pois import fetch_pois
from map.map_view import render_map
from map.styles import PRESETS

# ======================
# Page config
# ======================
st.set_page_config(
    page_title="City Map Art Studio",
    layout="wide",
)

st.title("City Map Art Studio")

# ======================
# Helper
# ======================
def distance_m(lat1, lon1, lat2, lon2):
    return int(
        math.sqrt(
            ((lat1 - lat2) * 111_320) ** 2 +
            ((lon1 - lon2) * 111_320) ** 2
        )
    )

# ======================
# Sidebar (LIVE controls)
# ======================
with st.sidebar:
    city = st.text_input("City / ZIP - Code", "Lugano")
    radius = st.slider("Radius (meters)", 500, 2500, 1200)

    preset_name = st.selectbox("Style Preset", PRESETS.keys())
    style = copy.deepcopy(PRESETS[preset_name])

    st.subheader("Point of Interest")
    show_categories = {
        "Attraction": st.checkbox("Attractions", True),
        "Historic": st.checkbox("Historic", True),
        "Museum": st.checkbox("Museums", True),
        "Restaurant": st.checkbox("Restaurants", False),
        "Nature": st.checkbox("Nature", False),
    }

    show_poi_list = st.checkbox("Show places table", value=False)

    st.subheader("Fine tuning")

    for layer in ["building", "water", "green", "road", "poi"]:
        with st.expander(layer.capitalize()):
            if "color" in style[layer]:
                hex_color = "#{:02x}{:02x}{:02x}".format(*style[layer]["color"])
                picked = st.color_picker(
                    "Color",
                    hex_color,
                    key=f"{layer}_color",
                )
                style[layer]["color"] = [
                    int(picked[i:i+2], 16) for i in (1, 3, 5)
                ]

            if "opacity" in style[layer]:
                style[layer]["opacity"] = st.slider(
                    "Opacity",
                    0.1,
                    1.0,
                    float(style[layer]["opacity"]),
                    0.05,
                    key=f"{layer}_opacity",
                )

            if "width" in style[layer]:
                style[layer]["width"] = st.slider(
                    "Width",
                    1,
                    6,
                    style[layer]["width"],
                    1,
                    key=f"{layer}_width",
                )

            if "size" in style[layer]:
                style[layer]["size"] = st.slider(
                    "Size",
                    20,
                    200,
                    style[layer]["size"],
                    10,
                    key=f"{layer}_size",
                )

# ======================
# Data loading (LIVE)
# ======================
@st.cache_data
def load_data(city, radius):
    lat, lon, name = geocode_city(city)
    osm = fetch_osm(lat, lon, radius)
    pois = fetch_pois(lat, lon, radius)
    return lat, lon, name, osm, pois

try:
    lat, lon, name, osm, pois = load_data(city, radius)

    # --- Filter POIs ---
    filtered_pois = [
        p for p in pois
        if show_categories.get(p["category"], False)
    ]

    # --- Render map ---
    render_map(
        lat=lat,
        lon=lon,
        osm=osm,
        pois=filtered_pois,
        style=style,
        radius=radius,
        title=name,
    )

    # ======================
    # POI TABLE (instead of list)
    # ======================
    if show_poi_list and filtered_pois:
        st.markdown("### Selected places")

        table_rows = []
        for poi in filtered_pois:
            dist = distance_m(lat, lon, poi["lat"], poi["lon"])

            icon = {
                "Restaurant": "☕",
                "Historic": "🏛️",
                "Museum": "🖼️",
                "Nature": "🌿",
                "Attraction": "📍",
            }.get(poi["category"], "📍")

            table_rows.append(
                {
                    "": icon,
                    "Name": poi["name"],
                    "Category": poi["category"],
                    "Distance (m) from center": dist,
                }
            )

        df = pd.DataFrame(table_rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

except Exception:
    st.info("Enter a valid city to see the map.")
