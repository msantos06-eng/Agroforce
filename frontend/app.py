import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from fastapi import FastAPI
from db import SessionLocal
from models import User
from auth import verify_password, create_token

app = FastAPI()

@app.post("/login")
def login(email: str, password: str):

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "user not found"}

    if not verify_password(password, user.password):
        return {"error": "invalid password"}

    token = create_token({
        "user_id": user.id,
        "email": user.email
    })

    return {"access_token": token}
    @app.get("/farms")
def get_farms(user_id: int):

    db = SessionLocal()

    farms = db.query(Farm).filter(Farm.user_id == user_id).all()

    return [
        {
            "id": f.id,
            "name": f.name
        }
        for f in farms
    ]

API = "https://SEU-BACKEND.onrender.com"

st.title("🌾 Agro SaaS Enterprise")

# 🔐 LOGIN
email = st.text_input("Email")
password = st.text_input("Senha", type="password")

if st.button("Login"):

    res = requests.post(f"{API}/login", params={
        "email": email,
        "password": password
    }).json()

    if "access_token" in res:
        st.session_state["token"] = res["access_token"]
        st.success("Logado com sucesso!")

# 📊 DASHBOARD
if "token" in st.session_state:

    token = st.session_state["token"]

    user_id = 1  # (depois vem do JWT decode)

    farms = requests.get(
        f"{API}/farms?user_id={user_id}"
    ).json()

    st.subheader("🌾 Suas Fazendas")

    for f in farms:
        st.write(f"• {f['name']}") 

API = "https://SEU-BACKEND.onrender.com"

st.title("🌾 Agro SaaS - NDVI Platform")

# ======================
# 🔐 LOGIN / CADASTRO
# ======================
menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro"])

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Senha", type="password")

if menu == "Cadastro":

    if st.sidebar.button("Criar conta"):

        r = requests.post(f"{API}/register", params={
            "email": email,
            "password": password
        })

        st.success("Conta criada!")

if menu == "Login":

    if st.sidebar.button("Entrar"):

        r = requests.post(f"{API}/login", params={
            "email": email,
            "password": password
        }).json()

        if "plan" in r:
            st.session_state["user"] = r
            st.success(f"Logado! Plano: {r['plan']}")

API = "https://SEU-BACKEND.onrender.com"

st.title("🌾 Agro SaaS")

email = st.text_input("Email")

if st.button("🚀 Assinar PRO (R$49/mês)"):

    res = requests.post(f"{API}/create-checkout-session", params={
        "email": email
    }).json()

    st.markdown(f"[Clique para pagar]({res['url']})")
    if user["plan"] == "free":
    st.warning("Plano gratuito: limite de NDVI")
else:
    st.success("Plano PRO ativo")
        else:
            st.error("Erro login")
            @app.post("/reset-password")
def reset_password(email: str):

    # versão simples (produção usa email real)
    return {"msg": f"link enviado para {email}"} 

# ======================
# 🌾 SAAS APP
# ======================
if "user" in st.session_state:

    user = st.session_state["user"]

    farm_id = st.number_input("ID Fazenda", value=1)

    if st.button("Rodar NDVI Sentinel"):

        # 🔒 LIMITAÇÃO FREE
        if user["plan"] == "free":
            st.warning("Plano free: limite básico aplicado")

        res = requests.get(f"{API}/farm-ndvi/{farm_id}").json()

        st.metric("NDVI médio", res["mean_ndvi"])
        st.success(res["status"])

    # 🗺️ MAPA
    m = folium.Map(location=[-12.5, -45], zoom_start=6)
    st_folium(m, width=900, height=600)

else:
    st.warning("Faça login para acessar o sistema")

API = "https://SEU-BACKEND.onrender.com"

st.set_page_config(page_title="Agro SaaS Map", layout="wide")

st.title("🌍 Agro SaaS Map")

# 📡 buscar dados do backend
data = requests.get(f"{API}/farms").json()

# 🗺️ mapa base
m = folium.Map(location=[-12.5, -45], zoom_start=6)

# 🌍 desenhar GeoJSON do PostGIS
folium.GeoJson(data).add_to(m)

# 📍 render no Streamlit
st_folium(m, width=900, height=600)

st.title("🌾 Desenhar Fazenda")

# 🗺️ mapa base
m = folium.Map(location=[-12.5, -45], zoom_start=6)

# 🖊️ ferramenta de desenho
from folium.plugins import Draw

Draw(
    export=True,
    filename="farm.geojson",
    draw_options={
        "polygon": True,
        "rectangle": True,
        "circle": False,
        "marker": False
    }
).add_to(m)

output = st_folium(m, height=600, width=900)

# 📡 capturar desenho
if output and output.get("last_active_drawing"):

    geojson = output["last_active_drawing"]

    st.success("Fazenda desenhada!")

    st.json(geojson)

    # enviar para backend
    import requests

    API = "https://SEU-BACKEND.onrender.com"

    requests.post(f"{API}/farms", json=geojson)
    import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

API = "https://SEU-BACKEND.onrender.com"

st.title("🌾 Agro SaaS - NDVI + Área")

data = requests.get(f"{API}/farms").json()

m = folium.Map(location=[-12.5, -45], zoom_start=6)

for f in data["features"]:

    props = f["properties"]

    folium.GeoJson(
        f,
        tooltip=f"{props['name']} - {props['hectares']:.2f} ha"
    ).add_to(m)

st_folium(m, width=900, height=600) 

from fastapi import FastAPI
from sentinel import get_token
from ndvi_sentinel import get_ndvi
from analysis import compute_ndvi_mean
from db import SessionLocal
from models import Farm

import numpy as np

app = FastAPI()

@app.get("/farm-ndvi/{farm_id}")
def farm_ndvi(farm_id: int):

    db = SessionLocal()

    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    # 🔴 bbox simplificado (produção usa geom real)
    bbox = [[-46,-12], [-45,-12], [-45,-13], [-46,-13], [-46,-12]]

    token = "SENTINEL_TOKEN"

    ndvi_raw = get_ndvi(token, bbox)

    # simulação decode raster (produção usa rasterio)
    ndvi_array = np.random.rand(100,100)

    mean_ndvi = compute_ndvi_mean(ndvi_array)

    if mean_ndvi < 0.3:
        status = "Estresse crítico"
    elif mean_ndvi < 0.6:
        status = "Médio vigor"
    else:
        status = "Saudável"

    return {
        "farm_id": farm_id,
        "mean_ndvi": mean_ndvi,
        "status": status
    }
    from fastapi import FastAPI
from db import SessionLocal
from models import NDVIHistory

app = FastAPI()

@app.post("/ndvi/save")
def save_ndvi(farm_id: int, season: str, mean_ndvi: float):

    db = SessionLocal()

    record = NDVIHistory(
        farm_id=farm_id,
        season=season,
        mean_ndvi=mean_ndvi
    )

    db.add(record)
    db.commit()
    db.close()

    return {"status": "saved"}
    import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "https://SEU-BACKEND.onrender.com"

st.title("🌾 Dashboard NDVI Empresarial")

farm_id = st.number_input("ID Fazenda", value=1)

# =========================
# 📊 HISTÓRICO NDVI
# =========================
if st.button("Carregar Histórico NDVI"):

    data = requests.get(
        f"{API}/ndvi/history/{farm_id}"
    ).json()

    df = pd.DataFrame(data)

    st.subheader("📊 Evolução NDVI por Safra")

    fig = px.line(
        df,
        x="season",
        y="mean_ndvi",
        markers=True,
        title="NDVI por Safra"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# 🌱 RESUMO EXECUTIVO
# =========================
if st.button("Resumo Executivo"):

    data = requests.get(
        f"{API}/ndvi/history/{farm_id}"
    ).json()

    df = pd.DataFrame(data)

    st.metric("NDVI atual", df["mean_ndvi"].iloc[-1])
    st.metric("Safras analisadas", len(df))

    if df["mean_ndvi"].iloc[-1] < 0.3:
        st.error("Estresse crítico na lavoura")
    elif df["mean_ndvi"].iloc[-1] < 0.6:
        st.warning("Vigor médio")
    else:
        st.success("Lavoura saudável")