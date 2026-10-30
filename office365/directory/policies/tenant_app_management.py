from __future__ import annotations

from typing import Optional

from office365.directory.policies.app_management_application_configuration import AppManagementApplicationConfiguration
from office365.directory.policies.app_management_service_principal_configuration import (  # noqa: E501
    AppManagementServicePrincipalConfiguration,
)
from office365.directory.policies.base import PolicyBase
from office365.runtime.types.odata_property import odata


class TenantAppManagementPolicy(PolicyBase):
    """
    Tenant-wide application authentication method policy to enforce app management restrictions for all applications
    and service principals. This policy applies to all apps and service principals unless overridden when an
    appManagementPolicy is applied to the object.
    """

    @odata(name="applicationRestrictions")
    @property
    def application_restrictions(self) -> AppManagementApplicationConfiguration:
        """Gets the applicationRestrictions property"""
        return self.properties.get("applicationRestrictions", AppManagementApplicationConfiguration())

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @odata(name="servicePrincipalRestrictions")
    @property
    def service_principal_restrictions(self) -> AppManagementServicePrincipalConfiguration:
        """Gets the servicePrincipalRestrictions property"""
        return self.properties.get("servicePrincipalRestrictions", AppManagementServicePrincipalConfiguration())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TenantAppManagementPolicy"
