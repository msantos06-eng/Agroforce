from fastapi import HTTPException
import jwt
import datetime
import hashlib
from fastapi import FastAPI
from db import SessionLocal
from models import User
from auth import hash_password, verify_password
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "SUA_CHAVE_SUPER_SECRETA"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------
# HASH SENHA
# ------------------
def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

# ------------------
# JWT TOKEN
# ------------------
def create_token(data: dict):

    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(days=7)
    })

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

app = FastAPI()

# --------------------
# CADASTRO
# --------------------
@app.post("/register")
def register(email: str, password: str):

    db = SessionLocal()

    user = User(
        email=email,
        password_hash=hash_password(password),
        plan="free"
    )

    db.add(user)
    db.commit()
    db.close()

    return {"status": "ok"}


# --------------------
# LOGIN
# --------------------
@app.post("/login")
def login(email: str, password: str):

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "user not found"}

    if not verify_password(password, user.password_hash):
        return {"error": "invalid password"}

    return {
        "user_id": user.id,
        "plan": user.plan
    }
    from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    plan = Column(String)   

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hash_):
    return hash_password(password) == hash_

SECRET = "SUPER_SECRET_KEY"

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
        import jwt
import datetime

SECRET = "SUPER_SECRET"

def create_token(user_id):

    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }

    return jwt.encode(payload, SECRET, algorithm="HS256")