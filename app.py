"""
app.py

Main entry point of the City Map Art Studio web app.
Handles UI layout, user interaction, preset application,
data loading, and map rendering.
"""

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
# Session state
# ======================
# rerender: forces a full PyDeck redraw (important for Streamlit Cloud)
# applied_preset: currently active style preset
if "rerender" not in st.session_state:
    st.session_state.rerender = 0

if "applied_preset" not in st.session_state:
    st.session_state.applied_preset = list(PRESETS.keys())[0]

# ======================
# Page config
# ======================
st.set_page_config(
    page_title="City Map Art Studio",
    layout="wide",
)

st.title("City Map Art Studio")

# ======================
# Helper functions
# ======================
def distance_m(lat1, lon1, lat2, lon2):
    """Approximate distance in meters between two coordinates."""
    return int(
        math.sqrt(
            ((lat1 - lat2) * 111_320) ** 2 +
            ((lon1 - lon2) * 111_320) ** 2
        )
    )

def reset_style_widget_states():
    """
    Removes widget states for colors, sliders etc.
    This ensures that a newly applied preset is not overwritten
    by previous fine-tuning values.
    """
    for layer in ["building", "water", "green", "road", "poi"]:
        for suffix in ["color", "opacity", "width", "size"]:
            key = f"{layer}_{suffix}"
            if key in st.session_state:
                del st.session_state[key]

# ======================
# Sidebar
# ======================
with st.sidebar:
    city = st.text_input("City / ZIP - Code", "Lugano")
    radius = st.slider("Radius (meters)", 500, 2500, 1200)

    preset_name = st.selectbox("Style Preset", PRESETS.keys())

    # Explicitly apply a preset to avoid Streamlit Cloud state issues
    if st.button("Apply preset", type="primary"):
        st.session_state.applied_preset = preset_name
        reset_style_widget_states()
        st.session_state.rerender += 1

    # Style is always derived from the applied preset
    style = copy.deepcopy(PRESETS[st.session_state.applied_preset])

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

    # Live style customization
    for layer in ["building", "water", "green", "road", "poi"]:
        with st.expander(layer.capitalize()):
            if "color" in style[layer]:
                default_hex = "#{:02x}{:02x}{:02x}".format(*style[layer]["color"])
                picked = st.color_picker("Color", default_hex, key=f"{layer}_color")
                style[layer]["color"] = [int(picked[i:i+2], 16) for i in (1, 3, 5)]

            if "opacity" in style[layer]:
                style[layer]["opacity"] = st.slider(
                    "Opacity", 0.1, 1.0,
                    float(style[layer]["opacity"]),
                    0.05,
                    key=f"{layer}_opacity",
                )

            if "width" in style[layer]:
                style[layer]["width"] = st.slider(
                    "Width", 1, 6,
                    style[layer]["width"],
                    1,
                    key=f"{layer}_width",
                )

            if "size" in style[layer]:
                style[layer]["size"] = st.slider(
                    "Size", 20, 200,
                    style[layer]["size"],
                    10,
                    key=f"{layer}_size",
                )

# ======================
# Data loading
# ======================
@st.cache_data
def load_data(city, radius):
    """Fetches geocoding, OSM geometry and POIs."""
    lat, lon, name = geocode_city(city)
    osm = fetch_osm(lat, lon, radius)
    pois = fetch_pois(lat, lon, radius)
    return lat, lon, name, osm, pois

try:
    lat, lon, name, osm, pois = load_data(city, radius)

    filtered_pois = [
        p for p in pois
        if show_categories.get(p["category"], False)
    ]

    render_map(
        lat=lat,
        lon=lon,
        osm=osm,
        pois=filtered_pois,
        style=style,
        radius=radius,
        title=name,
        rerender_key=st.session_state.rerender,
    )

    if show_poi_list and filtered_pois:
        st.markdown("### Selected places")

        rows = [
            {
                "Name": poi["name"],
                "Category": poi["category"],
                "Distance (m)": distance_m(lat, lon, poi["lat"], poi["lon"]),
            }
            for poi in filtered_pois
        ]

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

except Exception:
    st.info("Enter a valid city to see the map.")
