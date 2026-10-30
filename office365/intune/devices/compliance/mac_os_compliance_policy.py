from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.requiredpasswordtype import (
        RequiredPasswordType,
    )
    from office365.intune.devices.threatprotectionlevel import (
        DeviceThreatProtectionLevel,
    )


class MacOSCompliancePolicy(Entity):
    @odata(name="deviceThreatProtectionEnabled")
    @property
    def device_threat_protection_enabled(self) -> Optional[bool]:
        """Gets the deviceThreatProtectionEnabled property"""
        return self.properties.get("deviceThreatProtectionEnabled", None)

    @odata(name="deviceThreatProtectionRequiredSecurityLevel")
    @property
    def device_threat_protection_required_security_level(self) -> DeviceThreatProtectionLevel:
        """Gets the deviceThreatProtectionRequiredSecurityLevel property"""
        from office365.intune.devices.threatprotectionlevel import (
            DeviceThreatProtectionLevel,
        )

        return self.properties.get(
            "deviceThreatProtectionRequiredSecurityLevel", DeviceThreatProtectionLevel.unavailable
        )

    @odata(name="firewallBlockAllIncoming")
    @property
    def firewall_block_all_incoming(self) -> Optional[bool]:
        """Gets the firewallBlockAllIncoming property"""
        return self.properties.get("firewallBlockAllIncoming", None)

    @odata(name="firewallEnabled")
    @property
    def firewall_enabled(self) -> Optional[bool]:
        """Gets the firewallEnabled property"""
        return self.properties.get("firewallEnabled", None)

    @odata(name="firewallEnableStealthMode")
    @property
    def firewall_enable_stealth_mode(self) -> Optional[bool]:
        """Gets the firewallEnableStealthMode property"""
        return self.properties.get("firewallEnableStealthMode", None)

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

    @odata(name="passwordRequiredType")
    @property
    def password_required_type(self) -> RequiredPasswordType:
        """Gets the passwordRequiredType property"""
        from office365.intune.devices.compliance.requiredpasswordtype import (
            RequiredPasswordType,
        )

        return self.properties.get("passwordRequiredType", RequiredPasswordType.deviceDefault)

    @odata(name="storageRequireEncryption")
    @property
    def storage_require_encryption(self) -> Optional[bool]:
        """Gets the storageRequireEncryption property"""
        return self.properties.get("storageRequireEncryption", None)

    @odata(name="systemIntegrityProtectionEnabled")
    @property
    def system_integrity_protection_enabled(self) -> Optional[bool]:
        """Gets the systemIntegrityProtectionEnabled property"""
        return self.properties.get("systemIntegrityProtectionEnabled", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MacOSCompliancePolicy"
