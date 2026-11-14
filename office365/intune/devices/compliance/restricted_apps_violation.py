from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.policyplatformtype import PolicyPlatformType
from office365.runtime.types.odata_property import odata, version


@version("beta")
class RestrictedAppsViolation(Entity):
    @odata(name="deviceConfigurationId")
    @property
    def device_configuration_id(self) -> Optional[str]:
        """Gets the deviceConfigurationId property"""
        return self.properties.get("deviceConfigurationId", None)

    @odata(name="deviceConfigurationName")
    @property
    def device_configuration_name(self) -> Optional[str]:
        """Gets the deviceConfigurationName property"""
        return self.properties.get("deviceConfigurationName", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="managedDeviceId")
    @property
    def managed_device_id(self) -> Optional[str]:
        """Gets the managedDeviceId property"""
        return self.properties.get("managedDeviceId", None)

    @odata(name="platformType")
    @property
    def platform_type(self) -> PolicyPlatformType:
        """Gets the platformType property"""
        return self.properties.get("platformType", PolicyPlatformType.android)

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestrictedAppsViolation"
