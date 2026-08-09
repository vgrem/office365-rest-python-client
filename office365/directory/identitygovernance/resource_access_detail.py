from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identitygovernance.resource_access_status import ResourceAccessStatus
from office365.directory.identitygovernance.resource_access_type import ResourceAccessType
from office365.runtime.client_value import ClientValue


@dataclass
class ResourceAccessDetail(ClientValue):
    accessType: ResourceAccessType = ResourceAccessType.none
    identifier: str | None = None
    isCrossPromptInjectionDetected: bool | None = None
    labelId: str | None = None
    name: str | None = None
    status: ResourceAccessStatus = ResourceAccessStatus.none
    storageId: str | None = None
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResourceAccessDetail"
