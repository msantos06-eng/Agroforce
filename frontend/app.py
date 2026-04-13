import streamlit as st
import numpy as np
import requests
from PIL import Image

from ndvi import calculate_ndvi
from vra import generate_vra_map, export_vra_csv
from sentinel import get_token, search_sentinel
from ndvi_map import create_ndvi_colored_map
from streamlit_folium import st_folium

try:
    from ai_agro import analyze_sentinel_ndvi
except ImportError:
    analyze_sentinel_ndvi = None

st.set_page_config(page_title="NDVI SaaS v2", layout="wide")

API_URL = "http://localhost:3000/python-api"

st.title("🌱 Agro SaaS Pro")

# =========================
# NDVI RÁPIDO
# =========================
if st.button("Rodar NDVI"):
    try:
        res = requests.get(f"{API_URL}/ndvi")
        data = res.json()
        st.success(data["status"])
        st.info(data["recommendation"])
        st.metric("NDVI médio", data["mean_ndvi"])
    except Exception as e:
        st.error(f"Erro API: {e}")

# =========================
# NDVI VIA BACKEND
# =========================
if st.button("Rodar NDVI (Backend)"):
    try:
        response = requests.get(f"{API_URL}/ndvi")
        data = response.json()
        st.success(data["status"])
        st.info(data["recommendation"])
    except Exception as e:
        st.error(f"Erro: {e}")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📷 Upload NDVI", "🛰️ Sentinel + IA", "📋 Registros"])

# =========================================================
# TAB 1 -- Upload NDVI
# =========================================================
with tab1:
    uploaded_file = st.file_uploader(
        "Upload imagem (drone ou satélite)",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)

        st.subheader("Imagem Original")
        st.image(image, use_container_width=True)

        ndvi = calculate_ndvi(np.random.rand(10, 10), np.random.rand(10, 10))

        st.subheader("🌿 NDVI")
        st.image(ndvi, use_container_width=True)

        ndvi_map = create_ndvi_colored_map(ndvi)
        st_folium(ndvi_map, width=900, height=500)

        zones = generate_vra_map(ndvi)
        df = export_vra_csv(zones)

        st.subheader("📦 VRA")
        st.dataframe(df)

# =========================================================
# TAB 2 -- Sentinel + IA
# =========================================================
with tab2:
    st.header("🛰️ NDVI Satélite + IA")

    if st.button("Buscar Sentinel + IA"):
        try:
            client_id = st.secrets["sh-c0dac085-be43-4a1a-846b-9f2007c39719"]
            client_secret = st.secrets["mquL3Z5gSzNGH8Dq4eAynUuczrC7P5UE"]

            token = get_token(client_id, client_secret)
            st.success("Conectado ao Sentinel!")

            bbox = "POLYGON((-46 -12, -46 -13, -45 -13, -45 -12, -46 -12))"
            data = search_sentinel(token, bbox, "2024-01-01", "2024-01-10")
            st.json(data)

            ndvi_fake = np.random.rand(20, 20)

            if analyze_sentinel_ndvi:
                result = analyze_sentinel_ndvi(ndvi_fake, 0.6, 27)
                st.success(result["status"])
                st.info(result["recommendation"])
            else:
                st.warning("IA não disponível")

        except Exception as e:
            st.error(f"Erro: {str(e)}")

    st.subheader("🧠 IA Agrícola")

    rainfall = 0.6
    temp = 27

    if st.button("Rodar IA Agrícola") and analyze_sentinel_ndvi:
        result = analyze_sentinel_ndvi(np.random.rand(10, 10), rainfall, temp)
        st.success(result["status"])
        st.info(result["recommendation"])

# =========================================================
# TAB 3 -- Registros (API local)
# =========================================================
with tab3:
    st.header("📋 Registros")

    if st.button("Carregar registros"):
        resp = requests.get(f"{API_URL}/registros")
        if resp.status_code == 200:
            dados = resp.json()
            if dados:
                st.dataframe(dados)
            else:
                st.info("Nenhum registro encontrado.")
        else:
            st.error("Erro ao buscar registros")

    st.subheader("Criar registro")
    with st.form("form_criar"):
        nome = st.text_input("Nome")
        descricao = st.text_area("Descrição")
        enviado = st.form_submit_button("Salvar")

    if enviado:
        resp = requests.post(f"{API_URL}/registros", json={
            "nome": nome,
            "descricao": descricao
        })
        if resp.status_code == 201:
            st.success("Registro criado!")
            st.json(resp.json())
        else:
            st.error(f"Erro: {resp.json().get('detail', 'Erro desconhecido')}")

    st.subheader("Deletar registro")
    id_deletar = st.number_input("ID para deletar", min_value=1, step=1)
    if st.button("Deletar"):
        resp = requests.delete(f"{API_URL}/registros/{int(id_deletar)}")
        if resp.status_code == 200:
            st.success(resp.json()["message"])
        else:
            st.error("Registro não encontrado")