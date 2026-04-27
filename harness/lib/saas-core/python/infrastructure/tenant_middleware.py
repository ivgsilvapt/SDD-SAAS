"""
Middleware para FastAPI e Django que extrai tenant_id do JWT e popula TenantContext.
"""
from __future__ import annotations

import base64
import json
from typing import Any, Callable, Optional

from ..domain.tenant_context import TenantContext


def decode_jwt_payload(token: str) -> dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    payload_b64 = parts[1]
    padding = 4 - len(payload_b64) % 4
    if padding != 4:
        payload_b64 += "=" * padding
    decoded = base64.urlsafe_b64decode(payload_b64)
    return json.loads(decoded)


def extract_tenant_id_from_payload(payload: dict[str, Any]) -> str:
    tenant_id = payload.get("tenant_id") or payload.get("tenantId")
    if not tenant_id or not isinstance(tenant_id, str):
        raise ValueError(
            "JWT missing tenant_id claim. "
            "Ensure the authentication token includes tenant context."
        )
    return tenant_id


# ── FastAPI middleware ─────────────────────────────────────────────────────────
try:
    from fastapi import Request, Response
    from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

    class TenantMiddleware(BaseHTTPMiddleware):
        """
        Uso em FastAPI:
            app.add_middleware(TenantMiddleware)
        Requer header: Authorization: Bearer <jwt>
        """

        async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
        ) -> Response:
            auth = request.headers.get("authorization", "")
            if not auth.startswith("Bearer "):
                return await call_next(request)

            token = auth.removeprefix("Bearer ")
            try:
                payload = decode_jwt_payload(token)
                tenant_id = extract_tenant_id_from_payload(payload)
                user_id: Optional[str] = payload.get("sub")
            except (ValueError, KeyError):
                return await call_next(request)

            async def _call() -> Response:
                return await call_next(request)

            return await TenantContext.run_async(tenant_id, _call, user_id)

except ImportError:
    pass


# ── Django middleware ──────────────────────────────────────────────────────────
try:
    from django.http import HttpRequest, HttpResponse

    class DjangoTenantMiddleware:
        """
        Uso em Django (settings.py MIDDLEWARE):
            "harness_saas_core.infrastructure.tenant_middleware.DjangoTenantMiddleware"
        """

        def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
            self.get_response = get_response

        def __call__(self, request: HttpRequest) -> HttpResponse:
            auth = request.META.get("HTTP_AUTHORIZATION", "")
            if auth.startswith("Bearer "):
                token = auth.removeprefix("Bearer ")
                try:
                    payload = decode_jwt_payload(token)
                    tenant_id = extract_tenant_id_from_payload(payload)
                    user_id = payload.get("sub")
                    return TenantContext.run(
                        tenant_id,
                        lambda: self.get_response(request),
                        user_id,
                    )
                except (ValueError, KeyError):
                    pass
            return self.get_response(request)

except ImportError:
    pass
