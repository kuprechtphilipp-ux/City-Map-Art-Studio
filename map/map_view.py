"""
map_view.py

Creates and renders the PyDeck map.
Handles layer creation, zoom logic, and visual styling.
"""

import pydeck as pdk
import streamlit as st

def calculate_zoom(radius):
    """Simple heuristic to map radius to zoom level."""
    if radius <= 500:
        return 15
    elif radius <= 1000:
        return 14
    elif radius <= 1500:
        return 13
    else:
        return 12

def render_map(lat, lon, osm, pois, style, radius, title, rerender_key):
    layers = []

    # Polygon layers: water, green areas, buildings
    for key in ["water", "green", "building"]:
        layers.append(
            pdk.Layer(
                "PolygonLayer",
                data=osm.get(key, []),
                get_polygon="path",
                get_fill_color=style[key]["color"],
                opacity=style[key].get("opacity", 1),
                stroked=False,
                id=f"{key}_{rerender_key}",  # force new GPU layer
            )
        )

    # Roads
    layers.append(
        pdk.Layer(
            "PathLayer",
            data=osm.get("road", []),
            get_path="path",
            get_color=style["road"]["color"],
            get_width=style["road"]["width"],
            width_scale=1,
            width_min_pixels=1,
            id=f"road_{rerender_key}",
        )
    )

    # Points of Interest
    if pois:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=pois,
                get_position="[lon, lat]",
                get_radius=style["poi"]["size"],
                get_fill_color=style["poi"]["color"],
                pickable=True,
                opacity=0.9,
                id=f"poi_{rerender_key}",
            )
        )

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=calculate_zoom(radius),
            pitch=0,
        ),
        map_style=None,
        tooltip={"text": "{name}"},
    )

    st.pydeck_chart(
        deck,
        use_container_width=True,
        key=f"deck_{rerender_key}",
    )

    st.markdown(
        f"<h2 style='text-align:center'>{title}</h2>",
        unsafe_allow_html=True,
    )
