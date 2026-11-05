from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CloudPcSourceDeviceImage(ClientValue):
    displayName: str | None = None
    resourceId: str | None = None
    subscriptionDisplayName: str | None = None
    subscriptionId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcSourceDeviceImage"
