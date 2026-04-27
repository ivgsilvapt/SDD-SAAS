"""
Logger estruturado via structlog com redação automática de PII.
"""
from __future__ import annotations

import logging
import os
from typing import Any

import structlog

PII_FIELDS = {
    "password", "token", "secret", "authorization",
    "credit_card", "ssn", "cpf", "cnpj", "api_key",
}


def _redact_processor(
    _logger: Any, _method: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    for field in PII_FIELDS:
        if field in event_dict:
            event_dict[field] = "[REDACTED]"
    return event_dict


def _add_context_processor(
    _logger: Any, _method: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    from .correlation import Correlation
    request_id = Correlation.get()
    if request_id:
        event_dict["request_id"] = request_id
    event_dict.setdefault("service", os.getenv("OTEL_SERVICE_NAME", os.getenv("APP_NAME", "app")))
    event_dict.setdefault("env", os.getenv("PYTHON_ENV", "production"))
    return event_dict


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            _redact_processor,
            _add_context_processor,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.ExceptionRenderer(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


configure_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = structlog.get_logger()
