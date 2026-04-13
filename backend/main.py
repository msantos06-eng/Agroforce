from fastapi import FastAPI
from db import SessionLocal
from models import Farm
import json
from fastapi import FastAPI
import stripe
from db import SessionLocal
from models import User

app = FastAPI()

stripe.api_key = "SUA_SECRET_KEY"

PRICE_ID = "price_xxxxxxx"

@app.post("/create-checkout-session")
def create_checkout(email: str):

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": PRICE_ID,
            "quantity": 1
        }],
        success_url="https://seu-app.com/sucesso",
        cancel_url="https://seu-app.com/cancelado",
        customer_email=email
    )

    return {"url": session.url}

app = FastAPI()

@app.get("/farms")
def get_farms():

    db = SessionLocal()

    try:
        farms = db.query(Farm).all()

        result = []

        for f in farms:

            # área em hectares (PostGIS raw SQL seria melhor em produção)
            area = db.execute(
                f"SELECT ST_Area(geom::geography)/10000 FROM farms WHERE id={f.id}"
            ).scalar()

            result.append({
                "type": "Feature",
                "geometry": json.loads(str(f.geom)),
                "properties": {
                    "id": f.id,
                    "name": f.name,
                    "hectares": area
                }
            })

        return {
            "type": "FeatureCollection",
            "features": result
        }

    finally:
        db.close()