from __future__ import annotations


class TenantId:
    def __init__(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("TenantId cannot be empty")
        if len(value) > 128:
            raise ValueError("TenantId cannot exceed 128 characters")
        self._value = value.strip()

    @classmethod
    def create(cls, value: str) -> TenantId:
        return cls(value)

    @classmethod
    def from_string(cls, value: str) -> TenantId:
        return cls(value)

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TenantId):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"TenantId({self._value!r})"
