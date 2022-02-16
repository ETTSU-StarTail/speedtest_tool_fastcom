from __future__ import annotations

import logging
import logging.config

log_formatter = (
    "%(levelname)s %(asctime)s - %(filename)s::%(module)s::%(funcName)s -> %(message)s"
)

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "basicFormatter": {
                "format": log_formatter,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "streamHandler": {
                "class": "logging.StreamHandler",
                "level": logging.DEBUG,
                "formatter": "basicFormatter",
            },
            "fileHandler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": logging.DEBUG,
                "formatter": "basicFormatter",
                "filename": "speedtest.log",
                "when": "MIDNIGHT",
            },
        },
        "root": {
            "handlers": ["fileHandler"],
            "level": logging.DEBUG,
        },
        "loggers": {
            "basicLogger": {
                "handlers": ["fileHandler"],
                "level": logging.INFO,
                "propagate": False,
            },
            "debugLogger": {
                "handlers": ["fileHandler"],
                "level": logging.DEBUG,
                "propagate": False,
            },
        },
    }
)

logger = logging.getLogger("basicLogger")


def call_temp() -> None:
    print(f"called {__name__}.")


if __name__ == "__main__":
    print(f"{__file__} はモジュールをインポートして使ってください。")
