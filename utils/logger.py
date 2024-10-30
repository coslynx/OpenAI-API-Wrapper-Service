import logging
import sys
from typing import Optional

from config.settings import settings

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Returns a configured logger instance.

    Args:
        name: The name of the logger. If None, defaults to the root logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a formatter for the logs
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create a stream handler for the console
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Create a file handler for logs if DEBUG is enabled
    if settings.DEBUG:
        file_handler = logging.FileHandler("app.log", mode="a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger