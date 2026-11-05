from __future__ import annotations

from office365.directory.delegatedadmin.accesscontainertype import (
    DelegatedAdminAccessContainerType,
)
from office365.runtime.client_value import ClientValue


class DelegatedAdminAccessContainer(ClientValue):
    accessContainerId: str | None = None
    accessContainerType: DelegatedAdminAccessContainerType = DelegatedAdminAccessContainerType.securityGroup

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DelegatedAdminAccessContainer"
