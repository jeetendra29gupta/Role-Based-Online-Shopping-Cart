"""
Application logging utilities.

This module provides a centralized logger factory that:
- Logs to both console and rotating log files
- Uses configuration values from Config
- Prevents duplicate handlers
- Is safe for reuse across the application

Usage:
    from src.utilities.logger import get_logger
    logger = get_logger(__name__)
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

from src.utilities.config import Config

try:
    os.makedirs(Config.LOG_DIR, exist_ok=True)
except OSError as exc:
    raise RuntimeError(
        f"Failed to create log directory: {Config.LOG_DIR}"
    ) from exc

LOG_FILE_PATH = os.path.join(Config.LOG_DIR, Config.LOG_FILE)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Create or retrieve a configured application logger.

    The logger includes:
    - Console logging
    - Rotating file logging
    - Standardized log format
    - Protection against duplicate handlers

    Args:
        name (Optional[str]): Logger name, typically __name__.

    Returns:
        logging.Logger: Configured logger instance.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """

    logger = logging.getLogger(name or "app")
    logger.setLevel(logging.INFO)

    # Prevent log propagation to root logger
    logger.propagate = False

    if logger.handlers:
        return logger

    try:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        console_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        console_handler.setFormatter(console_formatter)

        # File Handler (Rotating)
        file_handler = RotatingFileHandler(
            LOG_FILE_PATH,
            maxBytes=Config.MAX_BYTES,
            backupCount=Config.BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.INFO)

        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | "
            "%(filename)s:%(lineno)d | %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.debug("Logger initialized successfully")

    except Exception as exc:
        raise RuntimeError("Failed to initialize logger") from exc

    return logger
