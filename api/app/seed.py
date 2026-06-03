from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Admin, Product
from app.security import hash_password

PRODUCTS = [
    {
        "slug": "apex-maple-cue",
        "name": "Apex Maple Pool Cue",
        "description": "A 58-inch hard rock maple cue with a 13mm leather tip and a low-deflection shaft. Balanced for control on the break and finesse on the rail.",
        "price_cents": 18900,
        "category": "Cues",
        "stock": 24,
    },
    {
        "slug": "carbon-break-cue",
        "name": "Carbon Break Cue",
        "description": "Carbon-fiber composite shaft tuned for power breaks. Phenolic tip transfers maximum energy with minimal cue ball squirt.",
        "price_cents": 32900,
        "category": "Cues",
        "stock": 11,
    },
    {
        "slug": "tournament-ball-set",
        "name": "Tournament Ball Set",
        "description": "Regulation 2.25-inch phenolic resin balls, polished and weight-matched. The set every league table deserves.",
        "price_cents": 12900,
        "category": "Balls",
        "stock": 40,
    },
    {
        "slug": "pro-felt-chalk-3pk",
        "name": "Pro Felt Chalk (3-Pack)",
        "description": "High-grip tournament chalk that holds on the tip and stays off the cloth. Three cubes in classic billiard green.",
        "price_cents": 1500,
        "category": "Accessories",
        "stock": 120,
    },
    {
        "slug": "leather-cue-case-2x2",
        "name": "Leather Cue Case 2x2",
        "description": "Full-grain leather case holding two cues, two shafts, with a padded interior and a dedicated chalk pocket.",
        "price_cents": 14500,
        "category": "Cases",
        "stock": 18,
    },
    {
        "slug": "billiard-glove-left",
        "name": "Billiard Glove (Left Hand)",
        "description": "Breathable three-finger glove for a smooth, consistent bridge. Machine washable spandex blend.",
        "price_cents": 2200,
        "category": "Accessories",
        "stock": 75,
    },
    {
        "slug": "magnetic-table-brush",
        "name": "Magnetic Table Brush",
        "description": "Horsehair brush with a magnetic handle that lifts chalk dust without grinding it into the cloth.",
        "price_cents": 3400,
        "category": "Care",
        "stock": 33,
    },
    {
        "slug": "9ft-table-cover",
        "name": "9ft Table Cover",
        "description": "Heavy-duty fitted cover for nine-foot tables. Water-resistant top, soft felt lining to protect the rails.",
        "price_cents": 8900,
        "category": "Care",
        "stock": 27,
    },
]


def seed(db: Session) -> None:
    if db.scalar(select(func.count()).select_from(Product)) == 0:
        db.add_all(Product(**data) for data in PRODUCTS)

    admin = db.scalar(select(Admin).where(Admin.email == settings.admin_email))
    if admin is None:
        db.add(
            Admin(
                email=settings.admin_email,
                password_hash=hash_password(settings.admin_password),
            )
        )
    db.commit()
