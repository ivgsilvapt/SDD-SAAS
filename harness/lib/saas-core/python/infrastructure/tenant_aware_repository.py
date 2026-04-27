from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from ..domain.tenant_aware_entity import TenantAwareEntity
from ..domain.tenant_context import TenantContext

T = TypeVar("T", bound=TenantAwareEntity)


class TenantAwareRepository(ABC, Generic[T]):
    """
    Classe base para repositórios com isolamento automático por tenant.
    O filtro por tenant_id é aplicado implicitamente — impossível esquecer.
    """

    @property
    def current_tenant_id(self) -> str:
        return TenantContext.get_tenant_id()

    def assert_belongs_to_current_tenant(self, entity: Optional[T]) -> Optional[T]:
        if entity is None:
            return None
        return entity if entity.belongs_to(self.current_tenant_id) else None

    def filter_by_current_tenant(self, entities: list[T]) -> list[T]:
        tenant_id = self.current_tenant_id
        return [e for e in entities if e.belongs_to(tenant_id)]

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[T]: ...

    @abstractmethod
    async def save(self, entity: T) -> None: ...

    @abstractmethod
    async def delete(self, id: str) -> None: ...

    @abstractmethod
    async def find_all(self) -> list[T]: ...
