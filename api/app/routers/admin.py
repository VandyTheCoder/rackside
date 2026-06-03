from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, Product
from app.schemas import ProductIn, ProductOut, OrderOut
from app.security import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/products", response_model=list[ProductOut])
def list_all_products(db: Session = Depends(get_db)) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.created_at.desc())))


@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductIn, db: Session = Depends(get_db)) -> Product:
    if db.scalar(select(Product).where(Product.slug == payload.slug)):
        raise HTTPException(status_code=409, detail="Slug already exists")
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    return product


@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: str, payload: ProductIn, db: Session = Depends(get_db)
) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in payload.model_dump().items():
        setattr(product, key, value)
    db.commit()
    return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, db: Session = Depends(get_db)) -> None:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()


@router.get("/orders", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)) -> list[Order]:
    return list(db.scalars(select(Order).order_by(Order.created_at.desc())))
