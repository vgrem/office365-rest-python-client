from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource_request import (
    AccessPackageResourceRequest,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class EntitlementManagement(Entity):
    """The entitlement management singleton is the container for entitlement management resources,
    including accessPackageCatalog, connectedOrganization, and entitlementManagementSettings.
    """

    @property
    def resource_requests(self):
        """Represents a request to add or remove a resource to or from a catalog respectively."""
        return self.properties.get(
            "resourceRequests",
            EntityCollection(
                self.context,
                AccessPackageResourceRequest,
                ResourcePath("resourceRequests", self.resource_path),
            ),
        )
