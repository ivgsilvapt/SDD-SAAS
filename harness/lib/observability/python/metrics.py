"""
Métricas HTTP com prometheus_client.
"""
from __future__ import annotations

import time
from typing import Any, Callable

from prometheus_client import REGISTRY, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "route", "status_code"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route", "status_code"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)


def metrics_content() -> tuple[bytes, str]:
    """Retorna o conteúdo das métricas no formato Prometheus."""
    return generate_latest(REGISTRY), CONTENT_TYPE_LATEST


# ── FastAPI route ──────────────────────────────────────────────────────────────
try:
    from fastapi import APIRouter, Response

    metrics_router = APIRouter()

    @metrics_router.get("/metrics")
    async def prometheus_metrics() -> Response:
        content, content_type = metrics_content()
        return Response(content=content, media_type=content_type)

except ImportError:
    pass
