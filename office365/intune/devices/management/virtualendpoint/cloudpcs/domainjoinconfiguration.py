from office365.intune.devices.management.virtualendpoint.cloudpcs.domainjointype import CloudPcDomainJoinType
from office365.intune.devices.management.virtualendpoint.cloudpcs.regiongroup import CloudPcRegionGroup
from office365.runtime.client_value import ClientValue


class CloudPcDomainJoinConfiguration(ClientValue):
    def __init__(
        self,
        domain_join_type: CloudPcDomainJoinType = CloudPcDomainJoinType.none,
        on_premises_connection_id: str = None,
        region_group: CloudPcRegionGroup = CloudPcRegionGroup.none,
        region_name: str = None,
    ):
        self.domainJoinType = domain_join_type
        self.onPremisesConnectionId = on_premises_connection_id
        self.regionGroup = region_group
        self.regionName = region_name

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcDomainJoinConfiguration"
