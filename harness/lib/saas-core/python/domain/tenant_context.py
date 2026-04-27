from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class TenantContextData:
    tenant_id: str
    user_id: Optional[str] = None


_tenant_context: ContextVar[Optional[TenantContextData]] = ContextVar(
    "tenant_context", default=None
)


class TenantContext:
    @staticmethod
    def run(tenant_id: str, fn: Callable[[], T], user_id: Optional[str] = None) -> T:
        """Executa fn com o tenant_id definido no contexto."""
        token = _tenant_context.set(TenantContextData(tenant_id=tenant_id, user_id=user_id))
        try:
            return fn()
        finally:
            _tenant_context.reset(token)

    @staticmethod
    async def run_async(
        tenant_id: str,
        fn: Callable[[], Any],
        user_id: Optional[str] = None,
    ) -> Any:
        """Versão async de run() para uso com FastAPI/asyncio."""
        import asyncio
        token = _tenant_context.set(TenantContextData(tenant_id=tenant_id, user_id=user_id))
        try:
            result = fn()
            if asyncio.iscoroutine(result):
                return await result
            return result
        finally:
            _tenant_context.reset(token)

    @staticmethod
    def current() -> TenantContextData:
        ctx = _tenant_context.get()
        if ctx is None:
            raise RuntimeError(
                "TenantContext.current() called outside of a tenant context. "
                "Ensure your request handler sets up TenantContext via tenant middleware."
            )
        return ctx

    @staticmethod
    def current_or_none() -> Optional[TenantContextData]:
        return _tenant_context.get()

    @staticmethod
    def get_tenant_id() -> str:
        return TenantContext.current().tenant_id

    @staticmethod
    def try_get_tenant_id() -> Optional[str]:
        ctx = _tenant_context.get()
        return ctx.tenant_id if ctx else None
