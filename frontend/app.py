
import streamlit as st
import requests
from streamlit_folium import st_folium
import folium

API = "https://SEU-BACKEND.onrender.com"

st.set_page_config(page_title="Agro SaaS Enterprise", layout="wide")

st.title("🌱 Agro SaaS Enterprise")

farm_id = st.number_input("ID da Fazenda", value=1)

# LOGIN
if st.button("Login"):
    res = requests.get(f"{API}/login").json()
    st.success("Login OK")
    st.write(res["token"])

# NDVI
if st.button("Rodar NDVI da Fazenda"):

    res = requests.get(f"{API}/ndvi/{farm_id}").json()

    st.metric("NDVI médio", res["mean_ndvi"])
    st.success(res["status"])
    st.info(res["recommendation"])

    # MAPA
    m = folium.Map(location=[-12.5, -45], zoom_start=6)
    st_folium(m, width=800)