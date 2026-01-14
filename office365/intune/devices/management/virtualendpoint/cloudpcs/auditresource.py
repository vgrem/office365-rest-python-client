from office365.intune.devices.management.virtualendpoint.cloudpcs.auditproperty import CloudPcAuditProperty
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class CloudPcAuditResource(ClientValue):
    def __init__(
        self,
        display_name: str = None,
        modified_properties: ClientValueCollection[CloudPcAuditProperty] = ClientValueCollection(CloudPcAuditProperty),
        resource_id: str = None,
    ):
        self.displayName = display_name
        self.modifiedProperties = modified_properties
        self.resourceId = resource_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditResource"
