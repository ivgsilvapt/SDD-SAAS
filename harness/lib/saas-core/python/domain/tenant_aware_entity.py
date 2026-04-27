from __future__ import annotations

from abc import ABC
from datetime import datetime, timezone

from .tenant_id import TenantId


class TenantAwareEntity(ABC):
    def __init__(self, id: str, tenant_id: str, created_at: datetime | None = None) -> None:
        if not id:
            raise ValueError(f"{self.__class__.__name__}: id is required")
        if not tenant_id:
            raise ValueError(f"{self.__class__.__name__}: tenant_id is required")
        self.id = id
        self.tenant_id = tenant_id
        self.created_at = created_at or datetime.now(tz=timezone.utc)

    def get_tenant_id(self) -> TenantId:
        return TenantId.from_string(self.tenant_id)

    def belongs_to(self, tenant_id: str) -> bool:
        return self.tenant_id == tenant_id
