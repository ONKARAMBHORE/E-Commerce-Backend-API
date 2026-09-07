# Ecommerce Backend API

A Django REST Framework backend for an ecommerce application. It includes JWT authentication, products, cart, wishlist, coupons, orders, shipping, Razorpay payments, notifications, PostgreSQL, Redis, and Celery.

## Features

- User registration, login, JWT refresh, and role-based permissions
- Product, category, brand, image, and review APIs
- Cart, wishlist, coupon, shipping, and order management
- Cash on delivery and Razorpay payment integration
- Email and in-app notifications
- Swagger and ReDoc API documentation
- Pytest test configuration
- Docker Compose services for Django, PostgreSQL, Redis, and Celery

## Requirements

- Python 3.13+
- Docker Desktop for the containerized setup
- PostgreSQL and Redis when running Django locally

## Quick Start With Docker

1. Clone the repository and enter the project directory:

```powershell
git clone https://github.com/ONKARAMBHORE/E-Commerce-Backend-API.git
cd E-Commerce-Backend-API
```

2. Create local environment values:

```powershell
Copy-Item .env.example .env
```

Update `.env` with real email and Razorpay credentials if those features are needed. Never commit `.env`.

3. Build and start the complete stack:

```powershell
docker compose up --build
```

The API is available at `http://127.0.0.1:8000/`.

Run it in the background with `docker compose up -d --build`. Stop it with `docker compose down`.

## Local Development

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start PostgreSQL and Redis with Docker:

```powershell
docker compose up -d db redis
```

Copy `.env.example` to `.env`, then apply migrations and start Django:

```powershell
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver 8080
```

Open `http://127.0.0.1:8080/`.

Start Celery in a second terminal while Redis is running:

```powershell
celery -A ecommerce_backend worker --loglevel=info
```

## Environment Variables

The supported variables are documented in `.env.example`:

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Enable development mode |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | PostgreSQL credentials |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP credentials |
| `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` | Razorpay credentials |

Docker supplies `DB_HOST`, `DB_PORT`, `REDIS_URL`, `CELERY_BROKER_URL`, and `CELERY_RESULT_BACKEND` automatically.

## API Documentation

When the server is running:

- Swagger UI: `http://127.0.0.1:8080/api/docs/`
- ReDoc: `http://127.0.0.1:8080/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8080/api/schema/`

Main API prefixes are `/api/accounts/`, `/api/products/`, `/api/cart/`, `/api/orders/`, `/api/payments/`, `/api/shipping/`, `/api/wishlist/`, `/api/coupons/`, and `/api/notifications/`.

## Testing

Run all tests with pytest:

```powershell
pytest
```

Run a specific app:

```powershell
pytest apps/products/tests.py
```

Run tests inside Docker:

```powershell
docker compose run --rm web pytest
```

Tests require PostgreSQL. Start it first with `docker compose up -d db` when running pytest locally.

## Project Structure

```text
apps/                  Django feature applications
ecommerce_backend/     Django settings, URLs, WSGI, ASGI, and Celery
media/                 User-uploaded media directory
static/                Static assets
Dockerfile             Django container image
docker-compose.yml     Django, PostgreSQL, Redis, and Celery services
pytest.ini              Pytest-Django configuration
requirements.txt       Python dependencies
```

## Security Notes

- Do not commit `.env`, API keys, passwords, or private credentials.
- Use a strong unique `SECRET_KEY` outside local development.
- Set `DEBUG=0` and configure production `ALLOWED_HOSTS` before deployment.
- Review payment and email credentials before sharing the repository publicly.

## License

No license has been selected yet. Add a `LICENSE` file before publishing if you want others to reuse this project under a specific license.

## Author

Onkar Ambhore
