from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CloudPcSourceDeviceImage(ClientValue):
    def __init__(
        self,
        display_name: str | None = None,
        resource_id: str | None = None,
        subscription_display_name: str | None = None,
        subscription_id: str | None = None,
    ):
        self.displayName = display_name
        self.resourceId = resource_id
        self.subscriptionDisplayName = subscription_display_name
        self.subscriptionId = subscription_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcSourceDeviceImage"
