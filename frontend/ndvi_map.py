import numpy as np
import folium

def create_ndvi_colored_map(ndvi: np.ndarray, center: list = [-12.5, -45.5]) -> folium.Map:
    m = folium.Map(location=center, zoom_start=10)
    mean_ndvi = float(np.mean(ndvi))

    if mean_ndvi >= 0.5:
        color, label = "green", f"Vegetação saudável (NDVI: {mean_ndvi:.2f})"
    elif mean_ndvi >= 0.2:
        color, label = "orange", f"Vegetação moderada (NDVI: {mean_ndvi:.2f})"
    else:
        color, label = "red", f"Vegetação baixa (NDVI: {mean_ndvi:.2f})"

    folium.Marker(location=center, popup=label, icon=folium.Icon(color=color, icon="leaf")).add_to(m)
    return m