"""Centralized logging configuration for the eval-track application."""

import logging
import sys
from typing import Any, Dict, Optional


def setup_logging(level: Optional[str] = None) -> None:
    """Configure logging for the entire application.

    Args:
        level: Optional logging level to override the default INFO level.
    """
    logging_level = getattr(logging, level.upper()) if level else logging.INFO

    # Configure the root logger with a structured format
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s %(extra_fields)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    # Set level for third-party loggers to reduce noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


class StructuredLogger:
    """Logger wrapper that supports structured logging with extra fields."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def _format_extra(self, extra: Optional[Dict[str, Any]] = None) -> str:
        if not extra:
            return ""
        return f"| {' '.join(f'{k}={v}' for k, v in extra.items())}"

    def info(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log info message with optional extra fields."""
        self.logger.info(msg, extra={"extra_fields": self._format_extra(extra)})

    def error(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log error message with optional extra fields."""
        self.logger.error(msg, extra={"extra_fields": self._format_extra(extra)})

    def warning(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log warning message with optional extra fields."""
        self.logger.warning(msg, extra={"extra_fields": self._format_extra(extra)})


def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance for the given name."""
    return StructuredLogger(name)
