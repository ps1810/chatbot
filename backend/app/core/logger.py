import logging
import logging.config
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s",
        },
        "extended_formatter": {
            "format": "%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s   call_trace=%(pathname)s L%(lineno)-4d"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "detailed_console_handler":{
            "class": "logging.StreamHandler",
            "formatter": "extended_formatter"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "extended_formatter",
            "filename": LOG_FILE_PATH,
            "maxBytes": 10485760,
            "backupCount": 5
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "app":{
        "handlers": ["console", "detailed_console_handler", "file"],
        "level": "DEBUG"
    }
}

logging.config.dictConfig(logging_config)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)