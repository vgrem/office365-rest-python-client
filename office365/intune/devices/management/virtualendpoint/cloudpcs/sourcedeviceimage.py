from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CloudPcSourceDeviceImage(ClientValue):
    displayName: str | None = None
    resourceId: str | None = None
    subscriptionDisplayName: str | None = None
    subscriptionId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcSourceDeviceImage"
