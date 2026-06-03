from contextlib import asynccontextmanager

import stripe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import admin, auth, checkout, products, webhooks
from app.seed import seed

stripe.api_key = settings.stripe_secret_key


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(title="Rackside API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api")
app.include_router(checkout.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
