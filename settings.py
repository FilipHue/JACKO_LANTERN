import os
import logging
import pathlib
from logging.config import dictConfig
import dotenv

dotenv.load_dotenv()

BOT_SECRET = os.getenv("TOKEN")

BASE_DIR = pathlib.Path(__file__).parent
CMDS_DIR = BASE_DIR / "commands"

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console1": {
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2": {
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "file": {
            'level': "INFO",
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w",
            'formatter': "standard"
        }
    },
    "loggers": {
        "bot": {
            'handlers': ['console1'],
            'level': "INFO",
            'propagate': False
        },
        "discord": {
            'handlers': ['console2', 'file'],
            'level': "INFO",
            'propagate': False
        }
    }
}

dictConfig(LOGGING_CONFIG)
