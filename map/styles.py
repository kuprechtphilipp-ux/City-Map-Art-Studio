"""
styles.py

Defines visual style presets for the map.
Each preset specifies colors and sizes for all layers.
"""

PRESETS = {
    "Tokyo Night": {
        "background": "#0B0D17",
        "building": {"color": [80, 80, 120], "opacity": 1},
        "water": {"color": [20, 30, 60], "opacity": 1},
        "green": {"color": [40, 60, 40], "opacity": 1},
        "road": {"color": [200, 200, 200], "width": 1},
        "poi": {"color": [255, 80, 80], "size": 140},
    },
    "Peach Art": {
        "background": "#F2F4CB",
        "building": {"color": [255, 192, 203], "opacity": 1},
        "water": {"color": [161, 227, 255], "opacity": 1},
        "green": {"color": [208, 240, 192], "opacity": 1},
        "road": {"color": [255, 204, 0], "width": 2},
        "poi": {"color": [60, 60, 60], "size": 120},
    },
    "Minimal Ink": {
        "background": "#FFFFFF",
        "building": {"color": [30, 30, 30], "opacity": 1},
        "water": {"color": [200, 200, 200], "opacity": 1},
        "green": {"color": [220, 220, 220], "opacity": 1},
        "road": {"color": [0, 0, 0], "width": 1},
        "poi": {"color": [0, 0, 0], "size": 80},
    },
}
