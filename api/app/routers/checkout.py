import json

import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Product
from app.schemas import CheckoutRequest, CheckoutResponse

router = APIRouter(tags=["checkout"])


@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout(payload: CheckoutRequest, db: Session = Depends(get_db)) -> CheckoutResponse:
    quantities = {item.slug: item.quantity for item in payload.items}
    products = db.scalars(
        select(Product).where(
            Product.slug.in_(quantities), Product.active.is_(True)
        )
    ).all()
    if not products:
        raise HTTPException(status_code=400, detail="Cart is empty")

    line_items = [
        {
            "quantity": quantities[product.slug],
            "price_data": {
                "currency": "usd",
                "unit_amount": product.price_cents,
                "product_data": {"name": product.name},
            },
        }
        for product in products
    ]
    cart = [[product.id, quantities[product.slug]] for product in products]

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        metadata={"cart": json.dumps(cart)},
        success_url=f"{settings.frontend_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.frontend_url}/cart",
    )
    return CheckoutResponse(url=session.url)
