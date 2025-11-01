A Flask-based loan service application featuring:
•	✅ Health check with database verification
•	📊 Prometheus metrics for observability
•	🧾 Structured JSON logging
•	📈 Grafana dashboard for visualization
________________________________________
🚀 How to Run the Application Locally
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
🧠 Design Decisions
Feature	Decision	Reason
Flask + Prometheus Exporter	prometheus_flask_exporter	Simplifies metrics instrumentation
PostgreSQL	Reliable & easy to Dockerize	Standard for backend data
JSON Logging	python-json-logger	Makes logs machine-parsable
Docker Compose	Multi-service orchestration	One command setup for local dev
Grafana + Prometheus	Industry standard for observability	Easy to monitor API metrics
________________________________________
⚖️ Trade-offs Considered
Option	Chosen	Reason
SQLite vs PostgreSQL	PostgreSQL	Production-grade & supports CI
Manual metrics vs Prometheus exporter	Exporter	Less code, standard format
Raw logging vs JSON logs	JSON	Easier for tools to parse
Separate services vs single container	Multiple	Matches real-world architecture
________________________________________
🚧 What Could Be Improved (Future Work)
•	Add authentication for /metrics and /health endpoints
•	Integrate Sentry for error monitoring
•	Include CI/CD deployment to AWS or GCP
•	More detailed Grafana dashboards
•	Unit tests with coverage reports
________________________________________
🧰 Troubleshooting
Problem	Cause	Solution
Flask API says “unhealthy”	DB not ready	Wait for db to pass healthcheck or restart containers
Prometheus shows “target down”	Wrong hostname	Use api:8000 inside Docker or host.docker.internal:8000 when external
Grafana login fails	Credentials wrong	Default → admin / admin
Port already in use	Previous instance running	Run docker-compose down then restart
Metrics not visible	Exporter misconfigured	Check /metrics endpoint manually
🧠 Design Decisions
1. Flask for API
•	Chosen because it’s simple, lightweight, and good for small projects.
•	Easy to create REST APIs and connect with databases.
2. PostgreSQL for Database
•	Reliable and commonly used in production.
•	Works well with Docker and SQLAlchemy.
•	Better than SQLite for handling multiple users and real data.
3. Prometheus and Grafana for Monitoring
•	Prometheus collects metrics (like request count, errors, response time).
•	Grafana helps to see the data in nice charts.
•	Used to make the project production-ready.
4. JSON Logging
•	Logs are in JSON format so they are easy to read by machines and tools.
•	Helps to track issues quickly.
•	Better than normal text logs for real monitoring systems.
5. Docker and Docker Compose
•	Makes it easy to run everything with one command:
docker-compose up
•	Works the same on all computers (no setup issues).
6. Environment Variables
•	Used .env files for different environments (dev, staging, prod).
•	Safer than hardcoding passwords or database details.
________________________________________
⚖️ Trade-offs
Choice	Trade-off	Reason
Flask	Not as powerful as Django	Easier for small projects
Prometheus/Grafana	More setup work	Adds great monitoring
PostgreSQL	Needs Docker setup	Real production database
JSON Logs	More complex	Easier for debugging later
________________________________________
🚀 Future Improvements
•	Add tests for all routes
•	Add login/authentication for /metrics and /health
•	Set up full CI/CD pipeline (auto build & deploy)
•	Add alerts in Prometheus (email or Slack)
•	Improve Grafana dashboard with more visuals
•	Use centralized logging (e.g., Loki)
•	Scale with Gunicorn and Nginx
🛠️ Troubleshooting
1. Containers not starting
Problem:
docker-compose up shows errors or services don’t start.
Fix:
•	Make sure Docker Desktop is running.
•	Run:
•	docker-compose down
•	docker-compose build --no-cache
•	docker-compose up -d
•	Check logs:
•	docker-compose logs -f
________________________________________
2. Database connection error
Problem:
Flask /health endpoint returns:
{"status": "unhealthy"}
Fix:
•	Check if the db container is healthy:
•	docker ps
Status should show (healthy).
•	Make sure your .env.production file has correct values:
•	POSTGRES_USER=postgres
•	POSTGRES_PASSWORD=postgres
•	POSTGRES_DB=appdb
•	Restart only the API after DB is ready:
•	docker-compose restart api
________________________________________
3. Prometheus not scraping metrics
Problem:
Prometheus UI (http://localhost:9090) shows target DOWN.
Fix:
•	Check Flask /metrics endpoint:
http://localhost:8000/metrics
→ It should show metric data.
•	If you’re running Flask locally and Prometheus in Docker, use:
•	targets: ["host.docker.internal:8000"]
in your prometheus.yml.
________________________________________
4. Grafana login issue
Default login:
•	URL → http://localhost:3030
•	Username → admin
•	Password → admin
If changed, reset in docker-compose.yml under:
environment:
  - GF_SECURITY_ADMIN_USER=admin
  - GF_SECURITY_ADMIN_PASSWORD=admin
________________________________________
5. How to check if everything is running correctly
✅ Flask API:
•	http://localhost:8000/health → should return
•	{"status": "healthy"}
✅ Metrics Endpoint:
•	http://localhost:8000/metrics → should show Prometheus metrics
✅ Prometheus UI:
•	http://localhost:9090 → "Targets" page should show Flask app as UP
✅ Grafana UI:
•	http://localhost:3030 → You can log in and add Prometheus as a data source


