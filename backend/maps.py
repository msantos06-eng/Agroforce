import folium
import numpy as np

def generate_map(ndvi):

    m = folium.Map(location=[-12.5, -45], zoom_start=6)

    folium.GeoJson(
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-46,-12], [-45,-12], [-45,-13], [-46,-13], [-46,-12]
                ]]
            }
        },
        name="Talhão"
    ).add_to(m)

    return m
    @app.get("/ndvi/history/{farm_id}")
def get_history(farm_id: int):

    db = SessionLocal()

    data = db.query(NDVIHistory).filter(
        NDVIHistory.farm_id == farm_id
    ).all()

    return [
        {
            "season": d.season,
            "mean_ndvi": d.mean_ndvi
        }
        for d in data
    ]