# Rackside

A small full-stack billiards storefront, split into a static-first frontend and
a standalone API:

- **`web/`** — Astro (SSR) storefront and admin, deployed to Vercel
- **`api/`** — FastAPI service (catalog, cart checkout, Stripe, orders, auth),
  deployed with Docker behind Nginx

The Astro server acts as a backend-for-frontend: the browser only ever talks to
Astro, which calls the FastAPI service server-side and holds the admin session
in an httpOnly cookie. The browser never sees the API directly.

```
Browser ─► Astro (Vercel) ─► FastAPI (Docker) ─► PostgreSQL
                                   └► Stripe (Checkout + webhooks)
```

## Features

- Catalog and product pages, server-rendered for SEO
- Cart with quantities, persisted client-side
- Stripe Checkout; prices are resolved server-side, never trusted from the client
- Order persistence via a signature-verified Stripe webhook
- Admin area (sign in, product CRUD, orders) gated by middleware

## Run it locally

Requires Docker and Node 20+.

```bash
# 1. API + PostgreSQL
cp .env.example .env          # fill in the Stripe test keys
docker compose up -d --build  # FastAPI on :8000, Postgres seeded on first boot

# 2. Frontend
cd web
npm install
npm run dev                   # Astro on http://localhost:4321
```

The store runs at http://localhost:4321; the admin area is at `/admin`.

### Stripe webhook (local)

```bash
stripe listen --forward-to localhost:8000/api/webhooks/stripe
```

Put the printed `whsec_...` in `STRIPE_WEBHOOK_SECRET`. Pay with Stripe's test
card `4242 4242 4242 4242`, any future expiry and CVC.

## Layout

```
api/app/          FastAPI app
  models.py       SQLAlchemy models
  schemas.py      Pydantic schemas
  security.py     bcrypt + JWT
  routers/        products, admin, auth, checkout, webhooks
web/src/
  pages/          routes (storefront + admin) and API endpoints
  components/      Astro components
  lib/            API client, auth cookie, helpers
  scripts/        client-side cart
```
