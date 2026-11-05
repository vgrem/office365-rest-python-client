from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.access_entity_type import AccessEntityType


class PackageAccessEntity(ClientValue):
    resourceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PackageAccessEntity"

    resourceType: AccessEntityType = AccessEntityType.user
