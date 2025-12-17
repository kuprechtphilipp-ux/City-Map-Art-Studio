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

    "Scandinavian Light": {
        "background": "#FAFAFA",
        "building": {"color": [180, 180, 180], "opacity": 1},
        "water": {"color": [200, 220, 230], "opacity": 1},
        "green": {"color": [210, 230, 210], "opacity": 1},
        "road": {"color": [120, 120, 120], "width": 2},
        "poi": {"color": [50, 50, 50], "size": 110},
    },

    "Architectural Beige": {
        "background": "#EFE6D8",
        "building": {"color": [190, 170, 140], "opacity": 1},
        "water": {"color": [180, 200, 210], "opacity": 1},
        "green": {"color": [200, 215, 190], "opacity": 1},
        "road": {"color": [120, 100, 80], "width": 2},
        "poi": {"color": [80, 60, 40], "size": 120},
    },

    "Blueprint Classic": {
        "background": "#001F3F",
        "building": {"color": [0, 64, 128], "opacity": 1},
        "water": {"color": [0, 26, 51], "opacity": 1},
        "green": {"color": [0, 51, 102], "opacity": 1},
        "road": {"color": [255, 255, 255], "width": 1},
        "poi": {"color": [255, 255, 255], "size": 100},
    },

    "Minimal Ink": {
        "background": "#FFFFFF",
        "building": {"color": [30, 30, 30], "opacity": 1},
        "water": {"color": [200, 200, 200], "opacity": 1},
        "green": {"color": [220, 220, 220], "opacity": 1},
        "road": {"color": [0, 0, 0], "width": 1},
        "poi": {"color": [0, 0, 0], "size": 80},
    },

    "Dark Poster": {
        "background": "#0E0E0E",
        "building": {"color": [50, 50, 50], "opacity": 1},
        "water": {"color": [20, 20, 20], "opacity": 1},
        "green": {"color": [35, 35, 35], "opacity": 1},
        "road": {"color": [120, 120, 120], "width": 1},
        "poi": {"color": [240, 240, 240], "size": 140},
    },

    "Warm Terracotta": {
        "background": "#F5EFEA",
        "building": {"color": [195, 135, 110], "opacity": 1},
        "water": {"color": [170, 200, 215], "opacity": 1},
        "green": {"color": [185, 205, 170], "opacity": 1},
        "road": {"color": [140, 110, 90], "width": 2},
        "poi": {"color": [90, 60, 40], "size": 120},
    },

    "Urban Concrete": {
        "background": "#ECECEC",
        "building": {"color": [120, 120, 120], "opacity": 1},
        "water": {"color": [170, 180, 190], "opacity": 1},
        "green": {"color": [190, 200, 190], "opacity": 1},
        "road": {"color": [70, 70, 70], "width": 2},
        "poi": {"color": [40, 40, 40], "size": 110},
    },
}

