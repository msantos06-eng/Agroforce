import streamlit as st
import sqlite3
from auth import criar_tabelas, cadastrar, login

st.set_page_config(page_title="Agro SaaS Pro", layout="wide")

criar_tabelas()

if "user" not in st.session_state:
    st.session_state.user = None

menu = ["Login", "Cadastrar"]
choice = st.sidebar.selectbox("Menu", menu)

# CADASTRO
if choice == "Cadastrar":
    st.title("Criar Conta")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        if cadastrar(user, password):
            st.success("Conta criada!")
        else:
            st.error("Usuário já existe")

# LOGIN
elif choice == "Login":
    st.title("Login")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if login(user, password):
            st.session_state.user = user
            st.success("Login realizado!")
        else:
            st.error("Erro no login")

# SISTEMA LOGADO
if st.session_state.user:
    st.sidebar.success(f"Usuário: {st.session_state.user}")

    menu2 = ["Dashboard", "Fazendas", "Talhões", "NDVI"]
    escolha = st.sidebar.selectbox("Sistema", menu2)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # DASHBOARD
    if escolha == "Dashboard":
        st.title("📊 Dashboard")
        fazendas = c.execute("SELECT COUNT(*) FROM fazendas WHERE user=?", (st.session_state.user,)).fetchone()[0]
        talhoes = c.execute("SELECT COUNT(*) FROM talhoes WHERE user=?", (st.session_state.user,)).fetchone()[0]

        col1, col2 = st.columns(2)
        col1.metric("Fazendas", fazendas)
        col2.metric("Talhões", talhoes)

    # FAZENDAS
    if escolha == "Fazendas":
        st.title("🌾 Fazendas")
        nome = st.text_input("Nome da Fazenda")

        if st.button("Salvar Fazenda"):
            c.execute("INSERT INTO fazendas (nome, user) VALUES (?,?)", (nome, st.session_state.user))
            conn.commit()
            st.success("Salvo!")

        for row in c.execute("SELECT * FROM fazendas WHERE user=?", (st.session_state.user,)):
            st.write(row)

    # TALHÕES
    if escolha == "Talhões":
        st.title("📍 Talhões")
        nome = st.text_input("Nome do Talhão")

        if st.button("Salvar Talhão"):
            c.execute("INSERT INTO talhoes (nome, user) VALUES (?,?)", (nome, st.session_state.user))
            conn.commit()
            st.success("Salvo!")

        for row in c.execute("SELECT * FROM talhoes WHERE user=?", (st.session_state.user,)):
            st.write(row)

    # NDVI
    if escolha == "NDVI":
        st.title("🛰️ NDVI")
        file = st.file_uploader("Enviar imagem NDVI")

        if file:
            st.image(file, caption="Imagem NDVI")

    conn.close()