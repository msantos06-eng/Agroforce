import numpy as np

def calculate_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    denominator = nir + red
    denominator = np.where(denominator == 0, 1e-10, denominator)
    ndvi = (nir - red) / denominator
    return np.clip(ndvi, -1, 1)