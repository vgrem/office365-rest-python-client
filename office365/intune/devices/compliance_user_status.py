from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.status import ComplianceStatus
from office365.runtime.types.odata_property import odata


class DeviceComplianceUserStatus(Entity):
    @odata(name="devicesCount")
    @property
    def devices_count(self) -> Optional[int]:
        """Gets the devicesCount property"""
        return self.properties.get("devicesCount", None)

    @odata(name="lastReportedDateTime")
    @property
    def last_reported_date_time(self) -> Optional[datetime]:
        """Gets the lastReportedDateTime property"""
        return self.properties.get("lastReportedDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> ComplianceStatus:
        """Gets the status property"""
        return self.properties.get("status", ComplianceStatus.unknown)

    @odata(name="userDisplayName")
    @property
    def user_display_name(self) -> Optional[str]:
        """Gets the userDisplayName property"""
        return self.properties.get("userDisplayName", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceComplianceUserStatus"
