# Flask Microloans API + Postgres (Docker)

Minimal REST API for microloans, built with Flask, SQLAlchemy, Alembic, and PostgreSQL (via Docker Compose).

## Quick start

```bash
# 1) Build and start services
docker compose up -d --build

# 2) Run DB migrations
docker compose exec api alembic upgrade head

# 3) Seed dummy data (idempotent)
docker compose exec api python scripts/seed.py

# 4) Hit endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/loans
```

## Configuration

See `.env.example` for env vars. By default:
- `DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/microloans`
- API listens on `localhost:8000`.

## API

- GET `/health` → `{ "status": "ok" }`
- GET `/api/loans` → list all loans
- GET `/api/loans/:id` → get loan by id
- POST `/api/loans` → create loan (status defaults to `pending`)

Example create:
```bash
curl -X POST http://localhost:8000/api/loans \
  -H 'Content-Type: application/json' \
  -d '{
    "borrower_id": "usr_india_999",
    "amount": 12000.50,
    "currency": "INR",
    "term_months": 6,
    "interest_rate_apr": 24.0
  }'
```

- GET `/api/stats` → aggregate stats: totals, avg, grouped by status/currency.

## Development

- App entrypoint: `wsgi.py` (`wsgi:app`)
- Flask app factory: `app/__init__.py`
- Models: `app/models.py`
- Migrations: `alembic/`

## Notes

- Amounts are validated server-side (0 < amount ≤ 50000).
- No authentication for this prototype.


---
## 🔧 Developer Documentation (By Ashwini)


1️⃣ Clone the Repository
git clone https://github.com/yourusername/loan-service.git
cd loan-service
2️⃣ Create an Environment File
Create .env.production in the root directory:
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=loan_db
DB_PORT=5432
API_PORT=8000
DATABASE_URL=postgresql+psycopg2://admin:admin@db:5432/loan_db
API_CMD=flask run --host=0.0.0.0 --port=8000
3️⃣ Run Docker Compose
docker-compose up --build
4️⃣ Verify the Setup
Service	URL	Description
Flask API	http://localhost:8000/health
Health Check
Prometheus	http://localhost:9090	Metrics Explorer
Grafana	http://localhost:3030	Metrics Dashboard
Nginx	http://localhost
Reverse Proxy
________________________________________
🧩 How to Switch Between Environments
You can switch between environments by modifying the .env file or creating new ones:
Environment	File	Purpose
Development	.env.dev	Local development, debug enabled
Staging	.env.staging	Pre-production testing
Production	.env.production	Live deployment
To switch:
cp .env.staging .env
docker-compose up --build
Each environment can have its own DATABASE_URL, LOG_LEVEL, and DEBUG configuration.
________________________________________
🔑 Environment Variables Explained
Variable	Description
POSTGRES_USER	Database username
POSTGRES_PASSWORD	Database password
POSTGRES_DB	PostgreSQL database name
DB_PORT	Exposed database port
API_PORT	Port for Flask API
DATABASE_URL	SQLAlchemy connection string
API_CMD	Command to start Flask
LOG_LEVEL	Logging verbosity (INFO, DEBUG, etc.)
________________________________________
⚙️ CI/CD Pipeline Overview
(Assuming GitHub Actions or similar)
1.	Build Stage:
o	Lint and test the Flask app.
o	Validate Dockerfile and docker-compose syntax.
2.	Test Stage:
o	Run Flask unit tests in an isolated container.
3.	Deploy Stage:
o	Push the Docker image to a registry (e.g., Docker Hub).
o	Automatically deploy to a server or cloud container environment.
Example GitHub Action (.github/workflows/ci.yml):
name: CI/CD Pipeline

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker-compose build
      - name: Run tests
        run: docker-compose run api pytest
________________________________________
🏗️ Architecture Diagram
                   ┌───────────────────────────────┐
                   │         User / Client          │
                   └───────┬───────────────────────┘
                           │
                      (HTTP Requests)
                           │
                   ┌───────▼──────────────────────┐
                   │          NGINX Proxy         │
                   └───────┬──────────────────────┘
                           │
                   ┌───────▼──────────────────────┐
                   │          Flask API           │
                   │ (Health, Metrics, Loans API) │
                   └───────┬──────────────────────┘
                           │
                   ┌───────▼──────────────────────┐
                   │         PostgreSQL DB        │
                   └──────────────────────────────┘
                           │
                   ┌───────▼──────────────────────┐
                   │         Prometheus           │
                   │ (Scrapes /metrics endpoint)  │
                   └───────┬──────────────────────┘
                           │
                   ┌───────▼──────────────────────┐
                   │          Grafana             │
                   │ (Visualize Metrics & Logs)   │
                   └──────────────────────────────┘
________________________________________
