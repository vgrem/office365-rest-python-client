from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class AndroidManagedAppProtection(Entity):
    @property
    def custom_browser_display_name(self) -> Optional[str]:
        """Gets the customBrowserDisplayName property"""
        return self.properties.get("customBrowserDisplayName", None)

    @property
    def custom_browser_package_id(self) -> Optional[str]:
        """Gets the customBrowserPackageId property"""
        return self.properties.get("customBrowserPackageId", None)

    @property
    def deployed_app_count(self) -> Optional[int]:
        """Gets the deployedAppCount property"""
        return self.properties.get("deployedAppCount", None)

    @property
    def disable_app_encryption_if_device_encryption_is_enabled(self) -> Optional[bool]:
        """Gets the disableAppEncryptionIfDeviceEncryptionIsEnabled property"""
        return self.properties.get("disableAppEncryptionIfDeviceEncryptionIsEnabled", None)

    @property
    def encrypt_app_data(self) -> Optional[bool]:
        """Gets the encryptAppData property"""
        return self.properties.get("encryptAppData", None)

    @property
    def minimum_required_patch_version(self) -> Optional[str]:
        """Gets the minimumRequiredPatchVersion property"""
        return self.properties.get("minimumRequiredPatchVersion", None)

    @property
    def minimum_warning_patch_version(self) -> Optional[str]:
        """Gets the minimumWarningPatchVersion property"""
        return self.properties.get("minimumWarningPatchVersion", None)

    @property
    def screen_capture_blocked(self) -> Optional[bool]:
        """Gets the screenCaptureBlocked property"""
        return self.properties.get("screenCaptureBlocked", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidManagedAppProtection"
