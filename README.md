# City Map Art Studio


CITYMAP_SIMPLE
│
├── app.py
├── requirements.txt
│
├── map
│   ├── map_view.py
│   ├── mask_layer.py        #Reserved for future mask-based layouts
│   └── styles.py
│
└── services
    ├── geocoding.py
    ├── osm.py
    └── pois.py



City Map Art Studio is a Streamlit web app for creating minimalist, stylized city maps using OpenStreetMap data.  
It renders buildings, water, green areas, roads, and points of interest as clean poster-style maps with live styling controls.

## Architecture Overview

- **app.py**  
  Main entry point. Handles UI, user inputs, data loading, caching, and orchestration.

- **services/**  
  External data access layer.  
  - `geocoding.py`: City name to coordinates via Nominatim  
  - `osm.py`: Buildings, water, green areas, roads via Overpass API  
  - `pois.py`: Points of interest via Overpass API

- **map/**  
  Rendering and styling layer.  
  - `map_view.py`: PyDeck map rendering and dynamic zoom  
  - `mask_layer.py`: Optional circular or rectangular map masks  
  - `styles.py`: Predefined visual style presets

## Tech Stack

- Python
- Streamlit
- PyDeck
- OpenStreetMap / Overpass API
- Pandas

## Run the App
streamlit run app.py

## Installation

```bash
pip install -r requirements.txt
