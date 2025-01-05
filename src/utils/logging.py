"""Custom logging configuration."""

import logging
import logging.config

from src.utils.config import Config


class Logging:
    """Custom logging configuration class."""

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "app.log",
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
            },
        },
    }

    @staticmethod
    def get_logger():
        """Return the custom logger."""
        logging.config.dictConfig(Logging.LOGGING_CONFIG)
        log_level = Config.get("logging.level")
        return logging.getLogger(__name__).setLevel(log_level)
