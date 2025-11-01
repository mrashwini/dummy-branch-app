import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Custom JSON log formatter for structured logging."""
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def configure_logging():
    """Configure Flask app logging to use JSON format."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    # Remove any default Flask log handlers to avoid duplicates
    for old_handler in root.handlers[:]:
        root.removeHandler(old_handler)
    
    root.addHandler(handler)
    logging.info("✅ JSON logging configured successfully.")
