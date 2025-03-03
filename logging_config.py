import logging
import logging.config

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOG_LEVEL = logging.DEBUG

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": LOG_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": LOG_LEVEL,
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
