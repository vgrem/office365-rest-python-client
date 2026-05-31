from office365.directory.objects.collection import DirectoryObjectCollection
from office365.directory.policies.base import PolicyBase
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AppManagementPolicy(PolicyBase):
    """
    Restrictions on app management operations for specific applications and service principals.
    If this resource is not configured for an application or service principal, the restrictions default
    to the settings in the tenantAppManagementPolicy object.
    """

    @odata(name="appliesTo")
    @property
    def applies_to(self) -> DirectoryObjectCollection:
        """Collection of applications and service principals to which the policy is applied."""
        return self.properties.get(
            "appliesTo",
            DirectoryObjectCollection(self.context, ResourcePath("appliesTo", self.resource_path)),
        )
