"""
TenantBuilder para construção de objetos Tenant em testes.
Padrão Builder com valores sensatos por padrão — sobrescreva apenas o necessário.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


TenantStatus = Literal["active", "suspended", "cancelled", "trial"]
TenantPlan = Literal["free", "basic", "pro", "enterprise"]


@dataclass
class TenantData:
    id: str
    slug: str
    name: str
    status: TenantStatus
    plan: TenantPlan
    created_at: datetime
    tenant_id: str = field(init=False)

    def __post_init__(self):
        self.tenant_id = self.id


class TenantBuilder:
    def __init__(self) -> None:
        self._id = "tenant-test-01"
        self._slug = "test-tenant"
        self._name = "Test Tenant"
        self._status: TenantStatus = "active"
        self._plan: TenantPlan = "pro"
        self._created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)

    def with_id(self, id: str) -> TenantBuilder:
        self._id = id
        return self

    def with_slug(self, slug: str) -> TenantBuilder:
        self._slug = slug
        return self

    def with_name(self, name: str) -> TenantBuilder:
        self._name = name
        return self

    def with_status(self, status: TenantStatus) -> TenantBuilder:
        self._status = status
        return self

    def with_plan(self, plan: TenantPlan) -> TenantBuilder:
        self._plan = plan
        return self

    def with_created_at(self, dt: datetime) -> TenantBuilder:
        self._created_at = dt
        return self

    def build(self) -> TenantData:
        return TenantData(
            id=self._id,
            slug=self._slug,
            name=self._name,
            status=self._status,
            plan=self._plan,
            created_at=self._created_at,
        )

    def build_many(self, count: int) -> list[TenantData]:
        return [
            TenantData(
                id=f"{self._id}-{i + 1}",
                slug=f"{self._slug}-{i + 1}",
                name=f"{self._name} {i + 1}",
                status=self._status,
                plan=self._plan,
                created_at=self._created_at,
            )
            for i in range(count)
        ]


def a_tenant() -> TenantBuilder:
    return TenantBuilder()
