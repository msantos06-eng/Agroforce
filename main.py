from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import hashlib
import os

app = FastAPI()

# 🔗 conexão banco (CORRIGIDO)
conn = psycopg2.connect(
    os.getenv("DATABASE_URL"),
    sslmode="require"
)
cursor = conn.cursor()

# ✅ cria tabela automaticamente
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    senha TEXT
)
""")
conn.commit()

# 📦 modelo
class Usuario(BaseModel):
    email: str
    senha: str

# 🔐 hash de senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# 📌 cadastro
@app.post("/cadastro")
def cadastro(user: Usuario):
    try:
        senha_hash = hash_senha(user.senha)

        cursor.execute(
            "INSERT INTO usuarios (email, senha) VALUES (%s, %s)",
            (user.email, senha_hash)
        )
        conn.commit()

        return {"status": "ok", "msg": "Usuário criado"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# 📌 login
@app.post("/login")
def login(user: Usuario):
    senha_hash = hash_senha(user.senha)

    cursor.execute(
        "SELECT * FROM usuarios WHERE email=%s AND senha=%s",
        (user.email, senha_hash)
    )

    result = cursor.fetchone()

    if result:
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")