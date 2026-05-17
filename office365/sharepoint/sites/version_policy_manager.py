from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.lists.version_policy_manager import VersionPolicyManager


class SiteVersionPolicyManager(Entity):
    """Manages versioning policies for a SharePoint site collection.

    Provides functionality to control document versioning settings including
    major version limits and automatic expiration policies.
    """

    @property
    def major_version_limit(self) -> Optional[int]:
        """Gets the maximum number of major versions allowed for documents.

        Returns:
            Optional[int]: The maximum number of major versions, or None if not set.
        """
        return self.properties.get("MajorVersionLimit", None)

    @property
    def version_policies(self) -> VersionPolicyManager:
        """Gets the version policies manager for detailed version control settings.

        Returns:
            VersionPolicyManager: The version policies manager instance.
        """
        return self.properties.get(
            "VersionPolicies",
            VersionPolicyManager(self.context, ResourcePath("VersionPolicies", self.resource_path)),
        )

    def inherit_tenant_settings(self):
        """Inherits version policy settings from the tenant-level configuration.

        Applies the tenant-wide version policy settings to this site collection,
        overriding any site-specific configurations.

        Returns:
            SiteVersionPolicyManager: The version policy manager instance
        """
        qry = ServiceOperationQuery(self, "InheritTenantSettings")
        self.context.add_query(qry)
        return self

    def set_auto_expiration(self):
        """Enables automatic expiration of document versions based on policy rules.

        Configures the site to automatically delete old document versions according
        to the established expiration policies and retention rules.

        Returns:
            SiteVersionPolicyManager: The version policy manager instance
        """
        qry = ServiceOperationQuery(self, "SetAutoExpiration")
        self.context.add_query(qry)
        return self

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "VersionPolicies": self.version_policies,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)
