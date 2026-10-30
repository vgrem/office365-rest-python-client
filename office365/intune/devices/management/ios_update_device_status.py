from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.status import ComplianceStatus
    from office365.intune.devices.configurations.ios.iosupdatesinstallstatus import (
        IosUpdatesInstallStatus,
    )


class IosUpdateDeviceStatus(Entity):
    @odata(name="complianceGracePeriodExpirationDateTime")
    @property
    def compliance_grace_period_expiration_date_time(self) -> Optional[datetime]:
        """Gets the complianceGracePeriodExpirationDateTime property"""
        return self.properties.get("complianceGracePeriodExpirationDateTime", datetime.min)

    @odata(name="deviceDisplayName")
    @property
    def device_display_name(self) -> Optional[str]:
        """Gets the deviceDisplayName property"""
        return self.properties.get("deviceDisplayName", None)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="deviceModel")
    @property
    def device_model(self) -> Optional[str]:
        """Gets the deviceModel property"""
        return self.properties.get("deviceModel", None)

    @odata(name="installStatus")
    @property
    def install_status(self) -> IosUpdatesInstallStatus:
        """Gets the installStatus property"""
        from office365.intune.devices.configurations.ios.iosupdatesinstallstatus import (
            IosUpdatesInstallStatus,
        )

        return self.properties.get("installStatus", IosUpdatesInstallStatus.deviceOsHigherThanDesiredOsVersion)

    @odata(name="lastReportedDateTime")
    @property
    def last_reported_date_time(self) -> Optional[datetime]:
        """Gets the lastReportedDateTime property"""
        return self.properties.get("lastReportedDateTime", datetime.min)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @odata(name="status")
    @property
    def status(self) -> ComplianceStatus:
        """Gets the status property"""
        from office365.intune.devices.compliance.status import ComplianceStatus

        return self.properties.get("status", ComplianceStatus.unknown)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

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
        return "microsoft.graph.IosUpdateDeviceStatus"
