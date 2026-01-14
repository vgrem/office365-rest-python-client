from office365.runtime.client_value import ClientValue


class CloudPcSourceDeviceImage(ClientValue):
    def __init__(
        self,
        display_name: str = None,
        resource_id: str = None,
        subscription_display_name: str = None,
        subscription_id: str = None,
    ):
        self.displayName = display_name
        self.resourceId = resource_id
        self.subscriptionDisplayName = subscription_display_name
        self.subscriptionId = subscription_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcSourceDeviceImage"
