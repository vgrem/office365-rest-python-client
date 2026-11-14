from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.managed.actionstate import ActionState
from office365.runtime.types.odata_property import odata, version


@version("beta")
class RemoteActionAudit(Entity):
    @odata(name="actionState")
    @property
    def action_state(self) -> ActionState:
        """Gets the actionState property"""
        return self.properties.get("actionState", ActionState.none)

    @odata(name="bulkDeviceActionId")
    @property
    def bulk_device_action_id(self) -> Optional[str]:
        """Gets the bulkDeviceActionId property"""
        return self.properties.get("bulkDeviceActionId", None)

    @odata(name="deviceDisplayName")
    @property
    def device_display_name(self) -> Optional[str]:
        """Gets the deviceDisplayName property"""
        return self.properties.get("deviceDisplayName", None)

    @odata(name="deviceIMEI")
    @property
    def device_imei(self) -> Optional[str]:
        """Gets the deviceIMEI property"""
        return self.properties.get("deviceIMEI", None)

    @odata(name="deviceOwnerUserPrincipalName")
    @property
    def device_owner_user_principal_name(self) -> Optional[str]:
        """Gets the deviceOwnerUserPrincipalName property"""
        return self.properties.get("deviceOwnerUserPrincipalName", None)

    @odata(name="initiatedByUserPrincipalName")
    @property
    def initiated_by_user_principal_name(self) -> Optional[str]:
        """Gets the initiatedByUserPrincipalName property"""
        return self.properties.get("initiatedByUserPrincipalName", None)

    @odata(name="managedDeviceId")
    @property
    def managed_device_id(self) -> Optional[str]:
        """Gets the managedDeviceId property"""
        return self.properties.get("managedDeviceId", None)

    @odata(name="requestDateTime")
    @property
    def request_date_time(self) -> Optional[datetime]:
        """Gets the requestDateTime property"""
        return self.properties.get("requestDateTime", None)

    @odata(name="userName")
    @property
    def user_name(self) -> Optional[str]:
        """Gets the userName property"""
        return self.properties.get("userName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RemoteActionAudit"
