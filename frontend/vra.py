import numpy as np
import pandas as pd

def generate_vra_map(ndvi: np.ndarray) -> np.ndarray:
    zones = np.zeros_like(ndvi, dtype=int)
    zones[ndvi < 0.2] = 1
    zones[(ndvi >= 0.2) & (ndvi < 0.5)] = 2
    zones[ndvi >= 0.5] = 3
    return zones

def export_vra_csv(zones: np.ndarray) -> pd.DataFrame:
    rows, cols = np.indices(zones.shape)
    df = pd.DataFrame({
        "linha": rows.flatten(),
        "coluna": cols.flatten(),
        "zona": zones.flatten(),
        "dose_recomendada_kg_ha": np.where(
            zones.flatten() == 1, 120,
            np.where(zones.flatten() == 2, 80, 40)
        ),
    })
    return df