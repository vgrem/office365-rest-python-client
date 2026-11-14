from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.managed.actionstate import ActionState
from office365.runtime.types.odata_property import odata, version


@version("beta")
class WindowsInformationProtectionWipeAction(Entity):
    @odata(name="lastCheckInDateTime")
    @property
    def last_check_in_date_time(self) -> Optional[datetime]:
        """Gets the lastCheckInDateTime property"""
        return self.properties.get("lastCheckInDateTime", None)

    @odata(name="status")
    @property
    def status(self) -> ActionState:
        """Gets the status property"""
        return self.properties.get("status", ActionState.none)

    @odata(name="targetedDeviceMacAddress")
    @property
    def targeted_device_mac_address(self) -> Optional[str]:
        """Gets the targetedDeviceMacAddress property"""
        return self.properties.get("targetedDeviceMacAddress", None)

    @odata(name="targetedDeviceName")
    @property
    def targeted_device_name(self) -> Optional[str]:
        """Gets the targetedDeviceName property"""
        return self.properties.get("targetedDeviceName", None)

    @odata(name="targetedDeviceRegistrationId")
    @property
    def targeted_device_registration_id(self) -> Optional[str]:
        """Gets the targetedDeviceRegistrationId property"""
        return self.properties.get("targetedDeviceRegistrationId", None)

    @odata(name="targetedUserId")
    @property
    def targeted_user_id(self) -> Optional[str]:
        """Gets the targetedUserId property"""
        return self.properties.get("targetedUserId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionWipeAction"
