def analyze_ndvi(ndvi):

    avg = ndvi.mean()

    if avg < 0.3:
        return "Estresse crítico", "Irrigação urgente"
    elif avg < 0.6:
        return "Médio vigor", "Monitorar nutrientes"
    return "Saudável", "Sem ação"