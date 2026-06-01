from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.virtualendpoint.cloudpcs.provisioningtype import CloudPcProvisioningType


class CloudPC(Entity):
    @property
    def aad_device_id(self) -> Optional[str]:
        """Gets the aadDeviceId property"""
        return self.properties.get("aadDeviceId", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def grace_period_end_date_time(self) -> datetime:
        """Gets the gracePeriodEndDateTime property"""
        return self.properties.get("gracePeriodEndDateTime", datetime.min)

    @property
    def image_display_name(self) -> Optional[str]:
        """Gets the imageDisplayName property"""
        return self.properties.get("imageDisplayName", None)

    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def managed_device_id(self) -> Optional[str]:
        """Gets the managedDeviceId property"""
        return self.properties.get("managedDeviceId", None)

    @property
    def managed_device_name(self) -> Optional[str]:
        """Gets the managedDeviceName property"""
        return self.properties.get("managedDeviceName", None)

    @property
    def on_premises_connection_name(self) -> Optional[str]:
        """Gets the onPremisesConnectionName property"""
        return self.properties.get("onPremisesConnectionName", None)

    @property
    def provisioning_policy_id(self) -> Optional[str]:
        """Gets the provisioningPolicyId property"""
        return self.properties.get("provisioningPolicyId", None)

    @property
    def provisioning_policy_name(self) -> Optional[str]:
        """Gets the provisioningPolicyName property"""
        return self.properties.get("provisioningPolicyName", None)

    @property
    def provisioning_type(self) -> CloudPcProvisioningType:
        """Gets the provisioningType property"""
        return self.properties.get("provisioningType", CloudPcProvisioningType.dedicated)

    @property
    def service_plan_id(self) -> Optional[str]:
        """Gets the servicePlanId property"""
        return self.properties.get("servicePlanId", None)

    @property
    def service_plan_name(self) -> Optional[str]:
        """Gets the servicePlanName property"""
        return self.properties.get("servicePlanName", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPC"
