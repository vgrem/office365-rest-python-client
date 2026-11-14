from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management.role_scope_tag_auto_assignment import RoleScopeTagAutoAssignment


@version("beta")
class RoleScopeTag(Entity):
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

    @odata(name="isBuiltIn", readonly=True)
    @property
    def is_built_in(self) -> Optional[bool]:
        """Gets the isBuiltIn property"""
        return self.properties.get("isBuiltIn", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RoleScopeTag"

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[RoleScopeTagAutoAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management.role_scope_tag_auto_assignment import RoleScopeTagAutoAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[RoleScopeTagAutoAssignment](
                self.context, RoleScopeTagAutoAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @require_permission(
        delegated=[
            "DeviceManagementRBAC.ReadWrite.All",
        ],
        application=[
            "DeviceManagementRBAC.ReadWrite.All",
        ],
    )
    def assign(
        self, assignments: ClientValueCollection[RoleScopeTagAutoAssignment]
    ) -> EntityCollection[RoleScopeTagAutoAssignment]:
        """assign operation.

        Args:
            assignments (ClientValueCollection[RoleScopeTagAutoAssignment]):
                assignments parameter
        """
        from office365.intune.devices.management.role_scope_tag_auto_assignment import RoleScopeTagAutoAssignment

        return_type = EntityCollection(self.context, RoleScopeTagAutoAssignment)
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, return_type)
        self.context.add_query(qry)
        return return_type
