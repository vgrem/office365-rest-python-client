from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.virtualendpoint.cloudpcs.provisioningpolicyimagetype import (  # noqa: E501
    CloudPcProvisioningPolicyImageType,
)
from office365.intune.devices.management.virtualendpoint.cloudpcs.provisioningtype import CloudPcProvisioningType
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.cloud_pc_windows_setting import CloudPcWindowsSetting
    from office365.intune.devices.management.virtualendpoint.cloudpcs.domainjoinconfiguration import (
        CloudPcDomainJoinConfiguration,
    )
    from office365.intune.devices.management.virtualendpoint.cloudpcs.provisioningpolicyautopatch import (
        CloudPcProvisioningPolicyAutopatch,
    )
    from office365.intune.devices.management.virtualendpoint.provisioningpolicies.microsoft_managed_desktop import (
        MicrosoftManagedDesktop,
    )
    from office365.security.cloud_pc_provisioning_policy_assignment import (
        CloudPcProvisioningPolicyAssignment,
    )


class CloudPcProvisioningPolicy(Entity):
    @odata(name="alternateResourceUrl")
    @property
    def alternate_resource_url(self) -> Optional[str]:
        """Gets the alternateResourceUrl property"""
        return self.properties.get("alternateResourceUrl", None)

    @odata(name="autopatch")
    @property
    def autopatch(self) -> CloudPcProvisioningPolicyAutopatch:
        """Gets the autopatch property"""
        from office365.intune.devices.management.virtualendpoint.cloudpcs.provisioningpolicyautopatch import (
            CloudPcProvisioningPolicyAutopatch,
        )

        return self.properties.get("autopatch", CloudPcProvisioningPolicyAutopatch())

    @odata(name="cloudPcGroupDisplayName")
    @property
    def cloud_pc_group_display_name(self) -> Optional[str]:
        """Gets the cloudPcGroupDisplayName property"""
        return self.properties.get("cloudPcGroupDisplayName", None)

    @odata(name="cloudPcNamingTemplate")
    @property
    def cloud_pc_naming_template(self) -> Optional[str]:
        """Gets the cloudPcNamingTemplate property"""
        return self.properties.get("cloudPcNamingTemplate", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="domainJoinConfigurations")
    @property
    def domain_join_configurations(self) -> ClientValueCollection[CloudPcDomainJoinConfiguration]:
        """Gets the domainJoinConfigurations property"""
        from office365.intune.devices.management.virtualendpoint.cloudpcs.domainjoinconfiguration import (
            CloudPcDomainJoinConfiguration,
        )

        return self.properties.get(
            "domainJoinConfigurations",
            ClientValueCollection[CloudPcDomainJoinConfiguration](CloudPcDomainJoinConfiguration),
        )

    @odata(name="enableSingleSignOn")
    @property
    def enable_single_sign_on(self) -> Optional[bool]:
        """Gets the enableSingleSignOn property"""
        return self.properties.get("enableSingleSignOn", None)

    @odata(name="gracePeriodInHours")
    @property
    def grace_period_in_hours(self) -> Optional[int]:
        """Gets the gracePeriodInHours property"""
        return self.properties.get("gracePeriodInHours", None)

    @odata(name="imageDisplayName")
    @property
    def image_display_name(self) -> Optional[str]:
        """Gets the imageDisplayName property"""
        return self.properties.get("imageDisplayName", None)

    @odata(name="imageId")
    @property
    def image_id(self) -> Optional[str]:
        """Gets the imageId property"""
        return self.properties.get("imageId", None)

    @odata(name="imageType")
    @property
    def image_type(self) -> CloudPcProvisioningPolicyImageType:
        """Gets the imageType property"""
        return self.properties.get("imageType", CloudPcProvisioningPolicyImageType.gallery)

    @odata(name="localAdminEnabled")
    @property
    def local_admin_enabled(self) -> Optional[bool]:
        """Gets the localAdminEnabled property"""
        return self.properties.get("localAdminEnabled", None)

    @odata(name="microsoftManagedDesktop")
    @property
    def microsoft_managed_desktop(self) -> MicrosoftManagedDesktop:
        """Gets the microsoftManagedDesktop property"""
        from office365.intune.devices.management.virtualendpoint.provisioningpolicies.microsoft_managed_desktop import (
            MicrosoftManagedDesktop,
        )

        return self.properties.get("microsoftManagedDesktop", MicrosoftManagedDesktop())

    @odata(name="provisioningType")
    @property
    def provisioning_type(self) -> CloudPcProvisioningType:
        """Gets the provisioningType property"""
        return self.properties.get("provisioningType", CloudPcProvisioningType.dedicated)

    @odata(name="windowsSetting")
    @property
    def windows_setting(self) -> CloudPcWindowsSetting:
        """Gets the windowsSetting property"""
        from office365.intune.devices.cloud_pc_windows_setting import (
            CloudPcWindowsSetting,
        )

        return self.properties.get("windowsSetting", CloudPcWindowsSetting())

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[CloudPcProvisioningPolicyAssignment]:
        """Gets the assignments property"""
        from office365.security.cloud_pc_provisioning_policy_assignment import (
            CloudPcProvisioningPolicyAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[CloudPcProvisioningPolicyAssignment](
                self.context, CloudPcProvisioningPolicyAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcProvisioningPolicy"
