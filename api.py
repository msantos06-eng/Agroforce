from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API ONLINE"}

@app.get("/talhoes/{user_id}")
def listar_talhoes(user_id: int):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT geojson FROM talhoes WHERE usuario_id=?", (user_id,))
    dados = c.fetchall()

    return {"talhoes": dados}