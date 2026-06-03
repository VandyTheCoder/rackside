from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.schemas import ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    stmt = select(Product).where(Product.active.is_(True)).order_by(Product.created_at.desc())
    return list(db.scalars(stmt))


@router.get("/{slug}", response_model=ProductOut)
def get_product(slug: str, db: Session = Depends(get_db)) -> Product:
    product = db.scalar(
        select(Product).where(Product.slug == slug, Product.active.is_(True))
    )
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
