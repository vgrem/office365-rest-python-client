from __future__ import annotations

from office365.directory.application_permission_type import ApplicationPermissionType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ApplicationResourcePermission(ClientValue):
    id: str | None = None
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationResourcePermission"

    type: ApplicationPermissionType = ApplicationPermissionType.role
