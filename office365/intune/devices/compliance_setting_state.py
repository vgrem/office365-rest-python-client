from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.status import ComplianceStatus


class DeviceComplianceSettingState(Entity):
    @odata(name="complianceGracePeriodExpirationDateTime")
    @property
    def compliance_grace_period_expiration_date_time(self) -> Optional[datetime]:
        """Gets the complianceGracePeriodExpirationDateTime property"""
        return self.properties.get("complianceGracePeriodExpirationDateTime", datetime.min)

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

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="setting")
    @property
    def setting(self) -> Optional[str]:
        """Gets the setting property"""
        return self.properties.get("setting", None)

    @odata(name="settingName")
    @property
    def setting_name(self) -> Optional[str]:
        """Gets the settingName property"""
        return self.properties.get("settingName", None)

    @odata(name="state")
    @property
    def state(self) -> ComplianceStatus:
        """Gets the state property"""
        from office365.intune.devices.compliance.status import ComplianceStatus

        return self.properties.get("state", ComplianceStatus.unknown)

    @odata(name="userEmail")
    @property
    def user_email(self) -> Optional[str]:
        """Gets the userEmail property"""
        return self.properties.get("userEmail", None)

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
        return "microsoft.graph.DeviceComplianceSettingState"
