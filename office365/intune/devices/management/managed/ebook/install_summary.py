from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class EBookInstallSummary(Entity):
    @odata(name="failedDeviceCount")
    @property
    def failed_device_count(self) -> Optional[int]:
        """Gets the failedDeviceCount property"""
        return self.properties.get("failedDeviceCount", None)

    @odata(name="failedUserCount")
    @property
    def failed_user_count(self) -> Optional[int]:
        """Gets the failedUserCount property"""
        return self.properties.get("failedUserCount", None)

    @odata(name="installedDeviceCount")
    @property
    def installed_device_count(self) -> Optional[int]:
        """Gets the installedDeviceCount property"""
        return self.properties.get("installedDeviceCount", None)

    @odata(name="installedUserCount")
    @property
    def installed_user_count(self) -> Optional[int]:
        """Gets the installedUserCount property"""
        return self.properties.get("installedUserCount", None)

    @odata(name="notInstalledDeviceCount")
    @property
    def not_installed_device_count(self) -> Optional[int]:
        """Gets the notInstalledDeviceCount property"""
        return self.properties.get("notInstalledDeviceCount", None)

    @odata(name="notInstalledUserCount")
    @property
    def not_installed_user_count(self) -> Optional[int]:
        """Gets the notInstalledUserCount property"""
        return self.properties.get("notInstalledUserCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EBookInstallSummary"
