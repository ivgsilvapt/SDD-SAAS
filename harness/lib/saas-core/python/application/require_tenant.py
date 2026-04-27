"""
Decorator que garante que TenantContext está populado antes de executar o método.
Lança RuntimeError se chamado fora de contexto de tenant.
"""
from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

from ..domain.tenant_context import TenantContext

F = TypeVar("F", bound=Callable[..., Any])


def require_tenant(fn: F) -> F:
    """
    Uso:
        class MyUseCase:
            @require_tenant
            async def execute(self, input: Input) -> Output:
                ...
    """
    @functools.wraps(fn)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        ctx = TenantContext.current_or_none()
        if ctx is None:
            raise RuntimeError(
                "require_tenant: operation requires an authenticated tenant context. "
                "Ensure the request passed through tenant middleware."
            )
        return await fn(*args, **kwargs)

    @functools.wraps(fn)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        ctx = TenantContext.current_or_none()
        if ctx is None:
            raise RuntimeError(
                "require_tenant: operation requires an authenticated tenant context. "
                "Ensure the request passed through tenant middleware."
            )
        return fn(*args, **kwargs)

    import asyncio
    if asyncio.iscoroutinefunction(fn):
        return async_wrapper  # type: ignore[return-value]
    return sync_wrapper  # type: ignore[return-value]
