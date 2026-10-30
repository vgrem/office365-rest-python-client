from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.requiredpasswordtype import RequiredPasswordType
from office365.intune.devices.threatprotectionlevel import DeviceThreatProtectionLevel
from office365.runtime.types.odata_property import odata


class IosCompliancePolicy(Entity):
    @odata(name="deviceThreatProtectionEnabled")
    @property
    def device_threat_protection_enabled(self) -> Optional[bool]:
        """Gets the deviceThreatProtectionEnabled property"""
        return self.properties.get("deviceThreatProtectionEnabled", None)

    @odata(name="deviceThreatProtectionRequiredSecurityLevel")
    @property
    def device_threat_protection_required_security_level(self) -> DeviceThreatProtectionLevel:
        """Gets the deviceThreatProtectionRequiredSecurityLevel property"""
        return self.properties.get(
            "deviceThreatProtectionRequiredSecurityLevel", DeviceThreatProtectionLevel.unavailable
        )

    @odata(name="managedEmailProfileRequired")
    @property
    def managed_email_profile_required(self) -> Optional[bool]:
        """Gets the managedEmailProfileRequired property"""
        return self.properties.get("managedEmailProfileRequired", None)

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

    @odata(name="passcodeBlockSimple")
    @property
    def passcode_block_simple(self) -> Optional[bool]:
        """Gets the passcodeBlockSimple property"""
        return self.properties.get("passcodeBlockSimple", None)

    @odata(name="passcodeExpirationDays")
    @property
    def passcode_expiration_days(self) -> Optional[int]:
        """Gets the passcodeExpirationDays property"""
        return self.properties.get("passcodeExpirationDays", None)

    @odata(name="passcodeMinimumCharacterSetCount")
    @property
    def passcode_minimum_character_set_count(self) -> Optional[int]:
        """Gets the passcodeMinimumCharacterSetCount property"""
        return self.properties.get("passcodeMinimumCharacterSetCount", None)

    @odata(name="passcodeMinimumLength")
    @property
    def passcode_minimum_length(self) -> Optional[int]:
        """Gets the passcodeMinimumLength property"""
        return self.properties.get("passcodeMinimumLength", None)

    @odata(name="passcodeMinutesOfInactivityBeforeLock")
    @property
    def passcode_minutes_of_inactivity_before_lock(self) -> Optional[int]:
        """Gets the passcodeMinutesOfInactivityBeforeLock property"""
        return self.properties.get("passcodeMinutesOfInactivityBeforeLock", None)

    @odata(name="passcodePreviousPasscodeBlockCount")
    @property
    def passcode_previous_passcode_block_count(self) -> Optional[int]:
        """Gets the passcodePreviousPasscodeBlockCount property"""
        return self.properties.get("passcodePreviousPasscodeBlockCount", None)

    @odata(name="passcodeRequired")
    @property
    def passcode_required(self) -> Optional[bool]:
        """Gets the passcodeRequired property"""
        return self.properties.get("passcodeRequired", None)

    @odata(name="passcodeRequiredType")
    @property
    def passcode_required_type(self) -> RequiredPasswordType:
        """Gets the passcodeRequiredType property"""
        return self.properties.get("passcodeRequiredType", RequiredPasswordType.deviceDefault)

    @odata(name="securityBlockJailbrokenDevices")
    @property
    def security_block_jailbroken_devices(self) -> Optional[bool]:
        """Gets the securityBlockJailbrokenDevices property"""
        return self.properties.get("securityBlockJailbrokenDevices", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosCompliancePolicy"
