from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.requiredpasswordtype import (
        RequiredPasswordType,
    )


class Windows10CompliancePolicy(Entity):
    @odata(name="bitLockerEnabled")
    @property
    def bit_locker_enabled(self) -> Optional[bool]:
        """Gets the bitLockerEnabled property"""
        return self.properties.get("bitLockerEnabled", None)

    @odata(name="codeIntegrityEnabled")
    @property
    def code_integrity_enabled(self) -> Optional[bool]:
        """Gets the codeIntegrityEnabled property"""
        return self.properties.get("codeIntegrityEnabled", None)

    @odata(name="earlyLaunchAntiMalwareDriverEnabled")
    @property
    def early_launch_anti_malware_driver_enabled(self) -> Optional[bool]:
        """Gets the earlyLaunchAntiMalwareDriverEnabled property"""
        return self.properties.get("earlyLaunchAntiMalwareDriverEnabled", None)

    @odata(name="mobileOsMaximumVersion")
    @property
    def mobile_os_maximum_version(self) -> Optional[str]:
        """Gets the mobileOsMaximumVersion property"""
        return self.properties.get("mobileOsMaximumVersion", None)

    @odata(name="mobileOsMinimumVersion")
    @property
    def mobile_os_minimum_version(self) -> Optional[str]:
        """Gets the mobileOsMinimumVersion property"""
        return self.properties.get("mobileOsMinimumVersion", None)

    @odata(name="osMaximumVersion")
    @property
    def os_maximum_version(self) -> Optional[str]:
        """Gets the osMaximumVersion property"""
        return self.properties.get("osMaximumVersion", None)

    @odata(name="osMinimumVersion")
    @property
    def os_minimum_version(self) -> Optional[str]:
        """Gets the osMinimumVersion property"""
        return self.properties.get("osMinimumVersion", None)

    @odata(name="passwordBlockSimple")
    @property
    def password_block_simple(self) -> Optional[bool]:
        """Gets the passwordBlockSimple property"""
        return self.properties.get("passwordBlockSimple", None)

    @odata(name="passwordExpirationDays")
    @property
    def password_expiration_days(self) -> Optional[int]:
        """Gets the passwordExpirationDays property"""
        return self.properties.get("passwordExpirationDays", None)

    @odata(name="passwordMinimumCharacterSetCount")
    @property
    def password_minimum_character_set_count(self) -> Optional[int]:
        """Gets the passwordMinimumCharacterSetCount property"""
        return self.properties.get("passwordMinimumCharacterSetCount", None)

    @odata(name="passwordMinimumLength")
    @property
    def password_minimum_length(self) -> Optional[int]:
        """Gets the passwordMinimumLength property"""
        return self.properties.get("passwordMinimumLength", None)

    @odata(name="passwordMinutesOfInactivityBeforeLock")
    @property
    def password_minutes_of_inactivity_before_lock(self) -> Optional[int]:
        """Gets the passwordMinutesOfInactivityBeforeLock property"""
        return self.properties.get("passwordMinutesOfInactivityBeforeLock", None)

    @odata(name="passwordPreviousPasswordBlockCount")
    @property
    def password_previous_password_block_count(self) -> Optional[int]:
        """Gets the passwordPreviousPasswordBlockCount property"""
        return self.properties.get("passwordPreviousPasswordBlockCount", None)

    @odata(name="passwordRequired")
    @property
    def password_required(self) -> Optional[bool]:
        """Gets the passwordRequired property"""
        return self.properties.get("passwordRequired", None)

    @odata(name="passwordRequiredToUnlockFromIdle")
    @property
    def password_required_to_unlock_from_idle(self) -> Optional[bool]:
        """Gets the passwordRequiredToUnlockFromIdle property"""
        return self.properties.get("passwordRequiredToUnlockFromIdle", None)

    @odata(name="passwordRequiredType")
    @property
    def password_required_type(self) -> RequiredPasswordType:
        """Gets the passwordRequiredType property"""
        from office365.intune.devices.compliance.requiredpasswordtype import (
            RequiredPasswordType,
        )

        return self.properties.get("passwordRequiredType", RequiredPasswordType.deviceDefault)

    @odata(name="requireHealthyDeviceReport")
    @property
    def require_healthy_device_report(self) -> Optional[bool]:
        """Gets the requireHealthyDeviceReport property"""
        return self.properties.get("requireHealthyDeviceReport", None)

    @odata(name="secureBootEnabled")
    @property
    def secure_boot_enabled(self) -> Optional[bool]:
        """Gets the secureBootEnabled property"""
        return self.properties.get("secureBootEnabled", None)

    @odata(name="storageRequireEncryption")
    @property
    def storage_require_encryption(self) -> Optional[bool]:
        """Gets the storageRequireEncryption property"""
        return self.properties.get("storageRequireEncryption", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows10CompliancePolicy"
