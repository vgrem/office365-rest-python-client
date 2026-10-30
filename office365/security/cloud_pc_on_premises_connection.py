from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectionstatus import (  # noqa: E501
    CloudPcOnPremisesConnectionStatus,
)
from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectionstatusdetail import (  # noqa: E501
    CloudPcOnPremisesConnectionStatusDetail,
)
from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectiontype import (  # noqa: E501
    CloudPcOnPremisesConnectionType,
)
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class CloudPcOnPremisesConnection(Entity):
    @odata(name="adDomainName")
    @property
    def ad_domain_name(self) -> Optional[str]:
        """Gets the adDomainName property"""
        return self.properties.get("adDomainName", None)

    @odata(name="adDomainPassword")
    @property
    def ad_domain_password(self) -> Optional[str]:
        """Gets the adDomainPassword property"""
        return self.properties.get("adDomainPassword", None)

    @odata(name="adDomainUsername")
    @property
    def ad_domain_username(self) -> Optional[str]:
        """Gets the adDomainUsername property"""
        return self.properties.get("adDomainUsername", None)

    @odata(name="alternateResourceUrl")
    @property
    def alternate_resource_url(self) -> Optional[str]:
        """Gets the alternateResourceUrl property"""
        return self.properties.get("alternateResourceUrl", None)

    @odata(name="connectionType")
    @property
    def connection_type(self) -> CloudPcOnPremisesConnectionType:
        """Gets the connectionType property"""
        return self.properties.get("connectionType", CloudPcOnPremisesConnectionType.hybridAzureADJoin)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="healthCheckPaused")
    @property
    def health_check_paused(self) -> Optional[bool]:
        """Gets the healthCheckPaused property"""
        return self.properties.get("healthCheckPaused", None)

    @odata(name="healthCheckStatus")
    @property
    def health_check_status(self) -> CloudPcOnPremisesConnectionStatus:
        """Gets the healthCheckStatus property"""
        return self.properties.get("healthCheckStatus", CloudPcOnPremisesConnectionStatus.pending)

    @odata(name="healthCheckStatusDetail")
    @property
    def health_check_status_detail(self) -> CloudPcOnPremisesConnectionStatusDetail:
        """Gets the healthCheckStatusDetail property"""
        return self.properties.get("healthCheckStatusDetail", CloudPcOnPremisesConnectionStatusDetail())

    @odata(name="inUse")
    @property
    def in_use(self) -> Optional[bool]:
        """Gets the inUse property"""
        return self.properties.get("inUse", None)

    @odata(name="inUseByCloudPc")
    @property
    def in_use_by_cloud_pc(self) -> Optional[bool]:
        """Gets the inUseByCloudPc property"""
        return self.properties.get("inUseByCloudPc", None)

    @odata(name="organizationalUnit")
    @property
    def organizational_unit(self) -> Optional[str]:
        """Gets the organizationalUnit property"""
        return self.properties.get("organizationalUnit", None)

    @odata(name="resourceGroupId")
    @property
    def resource_group_id(self) -> Optional[str]:
        """Gets the resourceGroupId property"""
        return self.properties.get("resourceGroupId", None)

    @odata(name="scopeIds")
    @property
    def scope_ids(self) -> StringCollection:
        """Gets the scopeIds property"""
        return self.properties.get("scopeIds", StringCollection())

    @odata(name="subnetId")
    @property
    def subnet_id(self) -> Optional[str]:
        """Gets the subnetId property"""
        return self.properties.get("subnetId", None)

    @odata(name="subscriptionId")
    @property
    def subscription_id(self) -> Optional[str]:
        """Gets the subscriptionId property"""
        return self.properties.get("subscriptionId", None)

    @odata(name="subscriptionName")
    @property
    def subscription_name(self) -> Optional[str]:
        """Gets the subscriptionName property"""
        return self.properties.get("subscriptionName", None)

    @odata(name="virtualNetworkId")
    @property
    def virtual_network_id(self) -> Optional[str]:
        """Gets the virtualNetworkId property"""
        return self.properties.get("virtualNetworkId", None)

    @odata(name="virtualNetworkLocation")
    @property
    def virtual_network_location(self) -> Optional[str]:
        """Gets the virtualNetworkLocation property"""
        return self.properties.get("virtualNetworkLocation", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcOnPremisesConnection"
