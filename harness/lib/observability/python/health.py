"""
Health endpoints /health/live e /health/ready para FastAPI.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional

HealthCheckFn = Callable[[], Any]
_checks: list[tuple[str, HealthCheckFn]] = []


def register_health_check(name: str, check: HealthCheckFn) -> None:
    _checks.append((name, check))


async def run_health_checks() -> dict[str, Any]:
    results: dict[str, Any] = {}
    overall = "ok"

    async def run_one(name: str, check: HealthCheckFn) -> None:
        nonlocal overall
        try:
            result = check()
            if asyncio.iscoroutine(result):
                await result
            results[name] = {"status": "ok"}
        except Exception as e:
            results[name] = {"status": "error", "error": str(e)}
            overall = "down"

    await asyncio.gather(*[run_one(n, c) for n, c in _checks])
    return {
        "status": overall,
        "checks": results,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


try:
    from fastapi import APIRouter
    from fastapi.responses import JSONResponse

    health_router = APIRouter()

    @health_router.get("/health/live")
    async def liveness() -> dict[str, str]:
        return {"status": "ok", "timestamp": datetime.now(tz=timezone.utc).isoformat()}

    @health_router.get("/health/ready")
    async def readiness() -> JSONResponse:
        result = await run_health_checks()
        status_code = 200 if result["status"] == "ok" else 503
        return JSONResponse(content=result, status_code=status_code)

except ImportError:
    pass
