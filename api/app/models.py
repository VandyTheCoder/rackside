from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _id() -> str:
    return uuid4().hex


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_id)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    price_cents: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, index=True)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_id)
    stripe_session_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String)
    amount_cents: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, default="paid")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_id)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[str | None] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String)
    price_cents: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped[Order] = relationship(back_populates="items")


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_id)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
