from flask import Blueprint, jsonify, current_app
from sqlalchemy import text
from app.extensions import db  # only if you have a db object setup

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    try:
        # Try a database connection check if available
        current_app.logger.info("Checking database connectivity...")
        # Example: db.session.execute(text("SELECT 1"))
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        current_app.logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
