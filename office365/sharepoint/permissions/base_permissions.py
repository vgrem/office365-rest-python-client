from typing import Any, Iterator, Self, Union

from office365.runtime.client_value import ClientValue
from office365.sharepoint.permissions.kind import PermissionKind


class BasePermissions(ClientValue):
    """Specifies a set of built-in permissions."""

    def __init__(self):
        super().__init__()
        self.Low: int = 0
        self.High: int = 0

    def __repr__(self):
        perms = self.permission_levels
        return (
            f"BasePermissions({', '.join(perms)})"
            if perms
            else "BasePermissions(Empty)"
        )

    def __iter__(self) -> Iterator[str]:
        for perm in PermissionKind:
            if perm != PermissionKind.EmptyMask and self.has(perm):
                yield perm.name

    def __contains__(self, perm: Union[PermissionKind, int]) -> bool:
        return self.has(perm)

    def set(self, perm: Union[PermissionKind, int]) -> None:
        """Sets a permission with support for both enum and raw integer values."""
        if isinstance(perm, int):
            perm = PermissionKind(perm)

        if perm == PermissionKind.FullMask:
            self.Low = self.High = 0xFFFF
        elif perm == PermissionKind.EmptyMask:
            self.Low = self.High = 0
        else:
            bit_pos = perm.value - 1
            mask = 1 << (bit_pos % 32)

            if bit_pos < 32:
                self.High |= mask
            elif 32 <= bit_pos < 64:
                self.Low |= mask

    def has(self, perm: Union[PermissionKind, int]) -> bool:
        """Checks if permission is set with support for both enum and integer values."""
        if isinstance(perm, int):
            perm = PermissionKind(perm)

        if perm == PermissionKind.EmptyMask:
            return True
        if perm == PermissionKind.FullMask:
            return self.Low == 0xFFFF and self.High == 0xFFFF

        bit_pos = perm.value - 1
        if not 0 <= bit_pos < 64:
            return False

        mask = 1 << (bit_pos % 32)
        return bool(self.High & mask) if bit_pos < 32 else bool(self.Low & mask)

    def clear_all(self):
        """Clears all permissions for the current instance."""
        self.High = 0
        self.Low = 0

    def to_json(self, json_format=None):
        return {"Low": str(self.Low), "High": str(self.High)}

    def set_property(self, k: str, v: Any, persist_changes: bool = True) -> Self:
        if k in ("Low", "High"):
            setattr(self, k, int(v))
        return self

    @property
    def permission_levels(self):
        """Gets permission levels"""
        return list(self)
