from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from config import Config  # ✅ removed leading dot for better import
import logging
from pythonjsonlogger import jsonlogger
import psycopg2


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # -----------------------------
    # JSON Structured Logging Setup
    # -----------------------------
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("🪵 Logging initialized with JSON formatter")

    # -----------------------------
    # Prometheus Metrics Setup
    # -----------------------------
    metrics = PrometheusMetrics(app, path="/metrics")
    metrics.info("app_info", "Application info", version="1.0.1")

    # Custom request counter
    @metrics.counter(
        "http_request_count_total",
        "Total HTTP requests",
        labels={"method": lambda: request.method, "endpoint": lambda: request.path},
    )
    def before_request():
        pass

    # -----------------------------
    # Health check route
    # -----------------------------
    @app.route("/health", methods=["GET"])
    def health():
        """Health check for app and database."""
        try:
            db_uri = app.config["SQLALCHEMY_DATABASE_URI"].replace(
                "postgresql+psycopg2", "postgresql"
            )
            conn = psycopg2.connect(db_uri, connect_timeout=3)
            conn.close()
            app.logger.info("Database connection successful")
            return jsonify({"status": "healthy"}), 200
        except Exception as e:
            app.logger.error(f"❌ Database health check failed: {e}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500

    # -----------------------------
    # Root route for basic test
    # -----------------------------
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"message": "Flask Monitoring App Running 🚀"}), 200

    app.logger.info("✅ Flask app started successfully and Prometheus metrics enabled")
    return app


# --------------------------------
# Run directly for local testing
# --------------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)
