import streamlit as st
import sqlite3
import numpy as np
from PIL import Image
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Agro SaaS IA", layout="wide")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

def criar_tabelas():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        senha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fazendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        usuario_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS talhoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        fazenda_id INTEGER
    )
    """)

    conn.commit()

criar_tabelas()

# ---------------- AUTH ----------------
def cadastrar(username, senha):
    cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, senha))
    conn.commit()

def login(username, senha):
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND senha=?", (username, senha))
    return cursor.fetchone()

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN UI ----------------
if st.session_state.user is None:
    st.title("🌱 Agro SaaS IA")

    menu = st.radio("Acesso", ["Login", "Cadastro"])

    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if menu == "Cadastro":
        if st.button("Cadastrar"):
            cadastrar(username, senha)
            st.success("Usuário criado!")

    if menu == "Login":
        if st.button("Entrar"):
            user = login(username, senha)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Login inválido")

# ---------------- APP PRINCIPAL ----------------
else:
    st.sidebar.success(f"Logado como: {st.session_state.user[1]}")

    menu = st.sidebar.selectbox("Menu", ["Fazendas", "Talhões", "NDVI"])

    user_id = st.session_state.user[0]

    # -------- FAZENDAS --------
    if menu == "Fazendas":
        st.title("🚜 Fazendas")

        nome = st.text_input("Nome da fazenda")

        if st.button("Salvar Fazenda"):
            cursor.execute("INSERT INTO fazendas (nome, usuario_id) VALUES (?, ?)", (nome, user_id))
            conn.commit()
            st.success("Salvo!")

        cursor.execute("SELECT * FROM fazendas WHERE usuario_id=?", (user_id,))
        fazendas = cursor.fetchall()

        for f in fazendas:
            st.write(f"🌾 {f[1]}")

    # -------- TALHÕES --------
    if menu == "Talhões":
        st.title("📍 Talhões")

        cursor.execute("SELECT * FROM fazendas WHERE usuario_id=?", (user_id,))
        fazendas = cursor.fetchall()

        fazenda_dict = {f[1]: f[0] for f in fazendas}

        if fazenda_dict:
            fazenda_nome = st.selectbox("Selecione a fazenda", list(fazenda_dict.keys()))
            fazenda_id = fazenda_dict[fazenda_nome]

            nome = st.text_input("Nome do talhão")

            if st.button("Salvar Talhão"):
                cursor.execute("INSERT INTO talhoes (nome, fazenda_id) VALUES (?, ?)", (nome, fazenda_id))
                conn.commit()
                st.success("Salvo!")

            cursor.execute("SELECT * FROM talhoes WHERE fazenda_id=?", (fazenda_id,))
            talhoes = cursor.fetchall()

            for t in talhoes:
                st.write(f"🧩 {t[1]}")

        else:
            st.warning("Crie uma fazenda primeiro.")

    # -------- NDVI --------
    if menu == "NDVI":
        st.title("🌍 NDVI")

        uploaded_file = st.file_uploader("Envie imagem (RGB simulada)")

        if uploaded_file:
            image = Image.open(uploaded_file)
            img = np.array(image)

            if img.shape[2] >= 3:
                nir = img[:, :, 0].astype(float)
                red = img[:, :, 1].astype(float)

                ndvi = (nir - red) / (nir + red + 0.01)

                st.image(ndvi, caption="NDVI", use_column_width=True)
            else:
                st.error("Imagem inválida")

    # -------- LOGOUT --------
    if st.sidebar.button("Sair"):
        st.session_state.user = None
        st.rerun()