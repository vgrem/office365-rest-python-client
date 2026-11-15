from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata, version
from office365.teams.schedule.shifts.role_permission import ShiftsRolePermission


@version("beta")
class ShiftsRoleDefinition(Entity):
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

    @odata(name="shiftsRolePermissions")
    @property
    def shifts_role_permissions(self) -> ClientValueCollection[ShiftsRolePermission]:
        """Gets the shiftsRolePermissions property"""
        return self.properties.get(
            "shiftsRolePermissions", ClientValueCollection[ShiftsRolePermission](ShiftsRolePermission)
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ShiftsRoleDefinition"
