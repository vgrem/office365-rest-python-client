from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version


@version("beta")
class WindowsInformationProtectionDeviceRegistration(Entity):
    @odata(name="deviceMacAddress")
    @property
    def device_mac_address(self) -> Optional[str]:
        """Gets the deviceMacAddress property"""
        return self.properties.get("deviceMacAddress", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="deviceRegistrationId")
    @property
    def device_registration_id(self) -> Optional[str]:
        """Gets the deviceRegistrationId property"""
        return self.properties.get("deviceRegistrationId", None)

    @odata(name="deviceType")
    @property
    def device_type(self) -> Optional[str]:
        """Gets the deviceType property"""
        return self.properties.get("deviceType", None)

    @odata(name="lastCheckInDateTime")
    @property
    def last_check_in_date_time(self) -> Optional[datetime]:
        """Gets the lastCheckInDateTime property"""
        return self.properties.get("lastCheckInDateTime", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionDeviceRegistration"

    @require_permission(
        delegated=[
            "DeviceManagementApps.ReadWrite.All",
        ],
        application=[
            "DeviceManagementApps.ReadWrite.All",
        ],
    )
    def wipe(self) -> Self:
        """wipe operation."""
        qry = ServiceOperationQuery(self, "wipe", None, {}, None, None)
        self.context.add_query(qry)
        return self
