from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class EntityPermission(ClientValue):
    canHaveAccess: bool | None = None
    existingAccessType: int | None = None
    hasAccess: bool | None = None
    inputEntity: str | None = None
    isPending: bool | None = None
    recipientDeniedReason: int | None = None
    resolvedEntity: str | None = None
    role: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.EntityPermission"
