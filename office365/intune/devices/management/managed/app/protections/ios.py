from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.managed.app.dataencryptiontype import ManagedAppDataEncryptionType


class IosManagedAppProtection(Entity):
    @property
    def app_data_encryption_type(self) -> ManagedAppDataEncryptionType:
        """Gets the appDataEncryptionType property"""
        return self.properties.get("appDataEncryptionType", ManagedAppDataEncryptionType.useDeviceSettings)

    @property
    def custom_browser_protocol(self) -> Optional[str]:
        """Gets the customBrowserProtocol property"""
        return self.properties.get("customBrowserProtocol", None)

    @property
    def deployed_app_count(self) -> Optional[int]:
        """Gets the deployedAppCount property"""
        return self.properties.get("deployedAppCount", None)

    @property
    def face_id_blocked(self) -> Optional[bool]:
        """Gets the faceIdBlocked property"""
        return self.properties.get("faceIdBlocked", None)

    @property
    def minimum_required_sdk_version(self) -> Optional[str]:
        """Gets the minimumRequiredSdkVersion property"""
        return self.properties.get("minimumRequiredSdkVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosManagedAppProtection"
