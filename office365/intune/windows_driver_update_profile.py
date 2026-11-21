from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.driver_update_profile_approval_type import DriverUpdateProfileApprovalType
from office365.intune.windows_driver_update_profile_inventory_sync_status import (
    WindowsDriverUpdateProfileInventorySyncStatus,
)
from office365.permissions import require_permission, requires_license
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.windows_driver_update_inventory import WindowsDriverUpdateInventory
    from office365.intune.windows_driver_update_profile_assignment import WindowsDriverUpdateProfileAssignment


@version("beta")
@requires_license("INTUNE_A")
class WindowsDriverUpdateProfile(Entity):
    @odata(name="approvalType")
    @property
    def approval_type(self) -> Optional[DriverUpdateProfileApprovalType]:
        """Gets the approvalType property"""
        return self.properties.get("approvalType", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="deploymentDeferralInDays")
    @property
    def deployment_deferral_in_days(self) -> Optional[int]:
        """Gets the deploymentDeferralInDays property"""
        return self.properties.get("deploymentDeferralInDays", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="deviceReporting")
    @property
    def device_reporting(self) -> Optional[int]:
        """Gets the deviceReporting property"""
        return self.properties.get("deviceReporting", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="inventorySyncStatus")
    @property
    def inventory_sync_status(self) -> Optional[WindowsDriverUpdateProfileInventorySyncStatus]:
        """Gets the inventorySyncStatus property"""
        return self.properties.get("inventorySyncStatus", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="newUpdates")
    @property
    def new_updates(self) -> Optional[int]:
        """Gets the newUpdates property"""
        return self.properties.get("newUpdates", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[WindowsDriverUpdateProfileAssignment]:
        """Gets the assignments property"""
        from office365.intune.windows_driver_update_profile_assignment import WindowsDriverUpdateProfileAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[WindowsDriverUpdateProfileAssignment](
                self.context, WindowsDriverUpdateProfileAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="driverInventories", navigation=True)
    @property
    def driver_inventories(self) -> EntityCollection[WindowsDriverUpdateInventory]:
        """Gets the driverInventories property"""
        from office365.intune.windows_driver_update_inventory import WindowsDriverUpdateInventory

        return self.properties.get(
            "driverInventories",
            EntityCollection[WindowsDriverUpdateInventory](
                self.context, WindowsDriverUpdateInventory, ResourcePath("driverInventories", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDriverUpdateProfile"

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def assign(self, assignments: ClientValueCollection[WindowsDriverUpdateProfileAssignment]) -> Self:
        """assign operation.

        Args:
            assignments (ClientValueCollection[WindowsDriverUpdateProfileAssignment]):
                assignments parameter
        """
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def sync_inventory(self) -> Self:
        """syncInventory operation."""
        qry = ServiceOperationQuery(self, "syncInventory", None, {}, None, None)
        self.context.add_query(qry)
        return self
