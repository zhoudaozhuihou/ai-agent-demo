import logging
import sys
from typing import Dict, Any
from pathlib import Path
import json
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """Custom formatter adding correlation ID and timestamp"""
    
    def format(self, record):
        # Add ISO timestamp if not present
        if not hasattr(record, 'timestamp'):
            record.timestamp = datetime.utcnow().isoformat()
            
        # Add correlation ID if not present
        if not hasattr(record, 'correlation_id'):
            record.correlation_id = 'undefined'
            
        return super().format(record)

def setup_logging(
    level: str = "INFO",
    log_file: str = None,
    config: Dict[str, Any] = None
) -> None:
    """
    Setup logging configuration
    
    Args:
        level: Logging level
        log_file: Optional log file path
        config: Optional logging configuration
    """
    # Create logs directory if logging to file
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # Base configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": CustomFormatter,
                "format": json.dumps({
                    "timestamp": "%(timestamp)s",
                    "level": "%(levelname)s",
                    "correlation_id": "%(correlation_id)s",
                    "message": "%(message)s",
                    "module": "%(module)s",
                    "function": "%(funcName)s",
                    "line": "%(lineno)d"
                })
            },
            "standard": {
                "()": CustomFormatter,
                "format": "%(timestamp)s [%(levelname)s] %(correlation_id)s: %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": sys.stdout
            }
        },
        "root": {
            "level": level,
            "handlers": ["console"]
        }
    }
    
    # Add file handler if log file specified
    if log_file:
        logging_config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": log_file
        }
        logging_config["root"]["handlers"].append("file")
    
    # Update with any custom config
    if config:
        logging_config.update(config)
    
    # Configure logging
    logging.config.dictConfig(logging_config)
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
