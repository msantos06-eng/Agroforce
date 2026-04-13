from fastapi import Request
import stripe
from db import SessionLocal
from models import User

stripe.api_key = "SUA_SECRET_KEY"
endpoint_secret = "WEBHOOK_SECRET"

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )

    # pagamento confirmado
    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]
        email = session["customer_email"]

        db = SessionLocal()

        user = db.query(User).filter(User.email == email).first()

        if user:
            user.plan = "pro"
            db.commit()

        db.close()

    return {"status": "ok"}