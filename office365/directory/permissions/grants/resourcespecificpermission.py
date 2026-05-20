from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class ResourceSpecificPermission(ClientValue):
    description: str | None = None
    displayName: str | None = None
    id: UUID | None = None
    isEnabled: bool | None = None
    value: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ResourceSpecificPermission"
