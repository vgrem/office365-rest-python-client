from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.status import ComplianceStatus
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementIntentUserState(Entity):
    @odata(name="deviceCount")
    @property
    def device_count(self) -> Optional[int]:
        """Gets the deviceCount property"""
        return self.properties.get("deviceCount", None)

    @odata(name="lastReportedDateTime")
    @property
    def last_reported_date_time(self) -> Optional[datetime]:
        """Gets the lastReportedDateTime property"""
        return self.properties.get("lastReportedDateTime", None)

    @odata(name="state")
    @property
    def state(self) -> ComplianceStatus:
        """Gets the state property"""
        return self.properties.get("state", ComplianceStatus.unknown)

    @odata(name="userName")
    @property
    def user_name(self) -> Optional[str]:
        """Gets the userName property"""
        return self.properties.get("userName", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementIntentUserState"
