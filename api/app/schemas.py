import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=2000)
    price_cents: int = Field(gt=0, le=1_000_000)
    category: str = Field(min_length=2, max_length=60)
    stock: int = Field(ge=0, le=100_000)
    image_url: str | None = Field(default=None, max_length=500)
    active: bool = True

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str) -> str:
        if not SLUG_PATTERN.match(value):
            raise ValueError("slug must be lowercase words separated by hyphens")
        return value


class ProductIn(ProductBase):
    pass


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: str


class CheckoutItem(BaseModel):
    slug: str
    quantity: int = Field(ge=1, le=99)


class CheckoutRequest(BaseModel):
    items: list[CheckoutItem] = Field(min_length=1, max_length=50)


class CheckoutResponse(BaseModel):
    url: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    price_cents: int
    quantity: int


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    amount_cents: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]
