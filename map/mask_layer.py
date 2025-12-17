import pydeck as pdk
import math

def hex_to_rgb(hex_color: str):
    """Convert hex color (#RRGGBB) to [R, G, B]."""
    hex_color = hex_color.lstrip("#")
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

def create_mask_layer(shape, lat, lon, radius, background_color):
    """
    Creates a polygon mask with a hole (circle or rectangle) in the center.
    Everything outside the hole is filled with background_color.
    """

    # --- Convert background color ---
    if isinstance(background_color, str):
        fill_color = hex_to_rgb(background_color)
    else:
        fill_color = background_color

    # --- 1. Outer polygon (large rectangle) ---
    delta = 180  # degrees
    outer = [
        [lon - delta, lat - delta],
        [lon + delta, lat - delta],
        [lon + delta, lat + delta],
        [lon - delta, lat + delta],
        [lon - delta, lat - delta],
    ]

    # --- 2. Inner hole ---
    if shape == "circle":
        inner = []
        steps = 64
        for i in range(steps):
            angle = 2 * math.pi * i / steps
            dx = (radius / 111_320) * math.cos(angle)
            dy = (radius / 111_320) * math.sin(angle)
            inner.append([lon + dx, lat + dy])
        inner.append(inner[0])

    else:  # rectangle
        d = radius / 111_320
        inner = [
            [lon - d, lat - d],
            [lon + d, lat - d],
            [lon + d, lat + d],
            [lon - d, lat + d],
            [lon - d, lat - d],
        ]

    return pdk.Layer(
        "PolygonLayer",
        data=[{"polygon": [outer, inner]}],
        get_polygon="polygon",
        get_fill_color=fill_color,
        stroked=False,
        pickable=False,
    )
