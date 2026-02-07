
# Backend (FastAPI)

BuyNow backend API built with **FastAPI** + **MongoDB** (Motor/Beanie).

## Run (local)

Prereqs: Python 3.12+ and a MongoDB connection string.

```bash
cd Backend

python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Settings currently load from .env.production by default
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- API root: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`


## Environment variables

Configuration is defined in `app/config/settings.py` and (by default) loads from `Backend/.env.production`.

Required:

- `MONGO_URL`
- `DATABASE_NAME`
- `JWT_ACCESS_SECRET_KEY`
- `JWT_REFRESH_SECRET_KEY`
- `JWT_ALGORITHM` (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `60`)
- `CLOUDNARY_CLOUD_NAME`
- `CLOUDNARY_API_KEY`
- `CLOUDNARY_API_SECRET`
- `SENDERS_EMAIL`
- `GMAIL_PASSWORD`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`

Security note: don’t commit real credentials/secrets in env files.

## API base path

All API routes are mounted under:

- `/api`

Route groups (prefixes):

- `/api/user`
- `/api/product`
- `/api/payment`
- `/api/admin`
- `/api/seller`
- `/api/address`
- `/api/email`
- `/api/common`

## One-off migration

There is a helper script for a product-field backfill:

```bash
cd Backend
python migration.py
```

