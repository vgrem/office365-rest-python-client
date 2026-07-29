from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.network_adapter import NetworkAdapter
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SensorSettings(ClientValue):
    description: str | None = None
    domainControllerDnsNames: StringCollection = field(default_factory=StringCollection)
    isDelayedDeploymentEnabled: bool | None = None
    networkAdapters: EntityCollection[NetworkAdapter] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.SensorSettings"
