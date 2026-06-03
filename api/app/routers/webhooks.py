import json

import stripe
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Order, OrderItem, Product

router = APIRouter(tags=["webhooks"])


def _fulfill(db: Session, session: stripe.checkout.Session) -> None:
    if db.scalar(select(Order).where(Order.stripe_session_id == session["id"])):
        return

    raw_cart = (session.get("metadata") or {}).get("cart")
    if not raw_cart:
        return

    entries = json.loads(raw_cart)
    products = {
        product.id: product
        for product in db.scalars(
            select(Product).where(Product.id.in_([pid for pid, _ in entries]))
        )
    }

    order = Order(
        stripe_session_id=session["id"],
        email=(session.get("customer_details") or {}).get("email") or "unknown",
        amount_cents=session.get("amount_total") or 0,
    )
    for product_id, quantity in entries:
        product = products.get(product_id)
        if product is None:
            continue
        order.items.append(
            OrderItem(
                product_id=product.id,
                name=product.name,
                price_cents=product.price_cents,
                quantity=quantity,
            )
        )
    db.add(order)
    db.commit()


@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
    if stripe_signature is None:
        raise HTTPException(status_code=400, detail="Missing signature")

    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.stripe_webhook_secret
        )
    except (ValueError, stripe.SignatureVerificationError) as error:
        raise HTTPException(status_code=400, detail="Invalid signature") from error

    if event["type"] == "checkout.session.completed":
        _fulfill(db, event["data"]["object"])

    return {"received": True}
