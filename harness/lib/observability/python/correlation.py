"""
Correlation ID via contextvars — propagado automaticamente via AsyncLocalStorage.
"""
from __future__ import annotations

import uuid
from contextvars import ContextVar
from typing import Optional

_request_id: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


class Correlation:
    @staticmethod
    def set(request_id: Optional[str] = None) -> str:
        rid = request_id or str(uuid.uuid4())
        _request_id.set(rid)
        return rid

    @staticmethod
    def get() -> Optional[str]:
        return _request_id.get()

    @staticmethod
    def require() -> str:
        rid = _request_id.get()
        if rid is None:
            raise RuntimeError("No requestId in current context")
        return rid
