import logging

from qllm.core.config import settings


def get_logging_level(log_level: str) -> int:
    level = 0
    if log_level == "INFO":
        level = logging.INFO
    elif log_level == "DEBUG":
        level = logging.DEBUG
    elif log_level == "WARNING":
        level = logging.WARNING
    else:
        level = logging.ERROR

    return level


def configure_logging():
    """
    Configures logging for the application. Logs are written to both
    console and a file named `log/app.log`.
    """
    logging_level = get_logging_level(settings.LOG_LEVEL)

    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("log/app.log"),
            logging.StreamHandler(),
        ],
    )
