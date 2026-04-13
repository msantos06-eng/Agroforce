import numpy as np

def analyze_sentinel_ndvi(ndvi: np.ndarray, rainfall: float, temp: float) -> dict:
    mean_ndvi = float(np.mean(ndvi))

    if mean_ndvi >= 0.6:
        status = "✅ Vegetação saudável"
        recommendation = "Manter manejo atual. Condições favoráveis."
    elif mean_ndvi >= 0.35:
        status = "⚠️ Vegetação moderada"
        recommendation = "Verificar irrigação e nutrição. Possível estresse hídrico."
    else:
        status = "🚨 Vegetação com estresse"
        recommendation = "Intervenção recomendada. Avaliar pragas, doenças ou déficit hídrico."

    if rainfall < 0.3:
        recommendation += " Chuva abaixo do ideal -- considere irrigação."
    if temp > 35:
        recommendation += " Temperatura elevada -- risco de estresse térmico."

    return {
        "status": status,
        "recommendation": recommendation,
        "mean_ndvi": round(mean_ndvi, 4),
        "rainfall": rainfall,
        "temperature": temp,
    }