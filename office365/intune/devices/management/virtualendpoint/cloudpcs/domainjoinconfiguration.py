from __future__ import annotations

from office365.intune.devices.management.virtualendpoint.cloudpcs.domainjointype import CloudPcDomainJoinType
from office365.intune.devices.management.virtualendpoint.cloudpcs.regiongroup import CloudPcRegionGroup
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CloudPcDomainJoinConfiguration(ClientValue):
    domainJoinType: CloudPcDomainJoinType = CloudPcDomainJoinType.none
    onPremisesConnectionId: str | None = None
    regionGroup: CloudPcRegionGroup = CloudPcRegionGroup.none
    regionName: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcDomainJoinConfiguration"
