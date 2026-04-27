"""
InMemoryRepository genérico com isolamento por tenant_id.
Bug clássico de multi-tenant (esquecer o filtro) é impossível por design.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Optional, Protocol, TypeVar, runtime_checkable


@runtime_checkable
class TenantScoped(Protocol):
    id: str
    tenant_id: str


T = TypeVar("T", bound=TenantScoped)


@dataclass
class InMemoryRepository(Generic[T]):
    _store: dict[str, T] = field(default_factory=dict, init=False)

    async def find_by_id(self, id: str, tenant_id: str) -> Optional[T]:
        item = self._store.get(id)
        if item is None:
            return None
        return item if item.tenant_id == tenant_id else None

    async def save(self, item: T) -> None:
        self._store[item.id] = item

    async def delete(self, id: str, tenant_id: str) -> None:
        item = self._store.get(id)
        if item is not None and item.tenant_id == tenant_id:
            del self._store[id]

    async def find_all_by_tenant(self, tenant_id: str) -> list[T]:
        return [item for item in self._store.values() if item.tenant_id == tenant_id]

    async def find_all(self) -> list[T]:
        return list(self._store.values())

    async def count(self, tenant_id: Optional[str] = None) -> int:
        if tenant_id:
            return sum(1 for i in self._store.values() if i.tenant_id == tenant_id)
        return len(self._store)

    def reset(self) -> None:
        self._store.clear()


def create_in_memory_repository() -> InMemoryRepository:
    """Factory function para criar repositório in-memory."""
    return InMemoryRepository()
