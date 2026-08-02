from office365.directory.policies.unifiedrolemanagement.unified_role_assignment_schedule_request import (
    UnifiedRoleAssignmentScheduleRequest,
)
from office365.directory.rolemanagement.unifiedrole.assignment import (
    UnifiedRoleAssignment,
)
from office365.directory.rolemanagement.unifiedrole.definition import (
    UnifiedRoleDefinition,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class RbacApplication(Entity):
    """Role management container for unified role definitions and role assignments for Microsoft 365 role-based
    access control (RBAC) providers. The role assignments support only a single principal and a single scope.
    Currently directory and entitlementManagement are the two RBAC providers supported.
    """

    @odata(name="roleAssignments")
    @property
    def role_assignments(self) -> EntityCollection[UnifiedRoleAssignment]:
        """Resource to grant access to users or groups."""
        return self.properties.get(
            "roleAssignments",
            EntityCollection(
                self.context,
                UnifiedRoleAssignment,
                ResourcePath("roleAssignments", self.resource_path),
            ),
        )

    @odata(name="roleDefinitions")
    @property
    def role_definitions(self) -> EntityCollection[UnifiedRoleDefinition]:
        """Resource representing the roles allowed by RBAC providers and the permissions assigned to the roles."""
        return self.properties.get(
            "roleDefinitions",
            EntityCollection(
                self.context,
                UnifiedRoleDefinition,
                ResourcePath("roleDefinitions", self.resource_path),
            ),
        )

    @odata(name="roleAssignmentScheduleRequests")
    @property
    def role_assignment_schedule_requests(
        self,
    ) -> EntityCollection[UnifiedRoleAssignmentScheduleRequest]:
        """Resource representing the roles allowed by RBAC providers and the permissions assigned to the roles."""
        return self.properties.get(
            "roleAssignmentScheduleRequests",
            EntityCollection(
                self.context,
                UnifiedRoleAssignmentScheduleRequest,
                ResourcePath("roleAssignmentScheduleRequests", self.resource_path),
            ),
        )
