from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.policies.multifactorauthconfiguration import MultiFactorAuthConfiguration
from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.azure_ad_registration_policy import (
        AzureADRegistrationPolicy,
    )
    from office365.intune.policies.azure_ad_join_policy import AzureADJoinPolicy
    from office365.intune.policies.local_admin_password_settings import (
        LocalAdminPasswordSettings,
    )


class DeviceRegistrationPolicy(Entity):
    """Represents the policy scope that controls quota restrictions, additional authentication, and authorization
    policies to register device identities to your organization."""

    @odata(name="azureADJoin")
    @property
    def azure_ad_join(self) -> AzureADJoinPolicy:
        """Gets the azureADJoin property"""
        from office365.intune.policies.azure_ad_join_policy import AzureADJoinPolicy

        return self.properties.get("azureADJoin", AzureADJoinPolicy())

    @odata(name="azureADRegistration")
    @property
    def azure_ad_registration(self) -> AzureADRegistrationPolicy:
        """Gets the azureADRegistration property"""
        from office365.directory.policies.azure_ad_registration_policy import (
            AzureADRegistrationPolicy,
        )

        return self.properties.get("azureADRegistration", AzureADRegistrationPolicy())

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

    @odata(name="localAdminPassword")
    @property
    def local_admin_password(self) -> LocalAdminPasswordSettings:
        """Gets the localAdminPassword property"""
        from office365.intune.policies.local_admin_password_settings import (
            LocalAdminPasswordSettings,
        )

        return self.properties.get("localAdminPassword", LocalAdminPasswordSettings())

    @odata(name="multiFactorAuthConfiguration")
    @property
    def multi_factor_auth_configuration(self) -> MultiFactorAuthConfiguration:
        """Gets the multiFactorAuthConfiguration property"""
        return self.properties.get("multiFactorAuthConfiguration", MultiFactorAuthConfiguration.notRequired)

    @odata(name="userDeviceQuota")
    @property
    def user_device_quota(self) -> Optional[int]:
        """Gets the userDeviceQuota property"""
        return self.properties.get("userDeviceQuota", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceRegistrationPolicy"
