from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.androidrequiredpasswordtype import (
        AndroidRequiredPasswordType,
    )
    from office365.intune.devices.threatprotectionlevel import (
        DeviceThreatProtectionLevel,
    )


class AndroidWorkProfileCompliancePolicy(Entity):
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

    @odata(name="minAndroidSecurityPatchLevel")
    @property
    def min_android_security_patch_level(self) -> Optional[str]:
        """Gets the minAndroidSecurityPatchLevel property"""
        return self.properties.get("minAndroidSecurityPatchLevel", None)

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

    @odata(name="passwordExpirationDays")
    @property
    def password_expiration_days(self) -> Optional[int]:
        """Gets the passwordExpirationDays property"""
        return self.properties.get("passwordExpirationDays", None)

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
    def password_required_type(self) -> AndroidRequiredPasswordType:
        """Gets the passwordRequiredType property"""
        from office365.intune.devices.compliance.androidrequiredpasswordtype import (
            AndroidRequiredPasswordType,
        )

        return self.properties.get("passwordRequiredType", AndroidRequiredPasswordType.deviceDefault)

    @odata(name="securityBlockJailbrokenDevices")
    @property
    def security_block_jailbroken_devices(self) -> Optional[bool]:
        """Gets the securityBlockJailbrokenDevices property"""
        return self.properties.get("securityBlockJailbrokenDevices", None)

    @odata(name="securityDisableUsbDebugging")
    @property
    def security_disable_usb_debugging(self) -> Optional[bool]:
        """Gets the securityDisableUsbDebugging property"""
        return self.properties.get("securityDisableUsbDebugging", None)

    @odata(name="securityPreventInstallAppsFromUnknownSources")
    @property
    def security_prevent_install_apps_from_unknown_sources(self) -> Optional[bool]:
        """Gets the securityPreventInstallAppsFromUnknownSources property"""
        return self.properties.get("securityPreventInstallAppsFromUnknownSources", None)

    @odata(name="securityRequireCompanyPortalAppIntegrity")
    @property
    def security_require_company_portal_app_integrity(self) -> Optional[bool]:
        """Gets the securityRequireCompanyPortalAppIntegrity property"""
        return self.properties.get("securityRequireCompanyPortalAppIntegrity", None)

    @odata(name="securityRequireGooglePlayServices")
    @property
    def security_require_google_play_services(self) -> Optional[bool]:
        """Gets the securityRequireGooglePlayServices property"""
        return self.properties.get("securityRequireGooglePlayServices", None)

    @odata(name="securityRequireSafetyNetAttestationBasicIntegrity")
    @property
    def security_require_safety_net_attestation_basic_integrity(self) -> Optional[bool]:
        """Gets the securityRequireSafetyNetAttestationBasicIntegrity property"""
        return self.properties.get("securityRequireSafetyNetAttestationBasicIntegrity", None)

    @odata(name="securityRequireSafetyNetAttestationCertifiedDevice")
    @property
    def security_require_safety_net_attestation_certified_device(self) -> Optional[bool]:
        """Gets the securityRequireSafetyNetAttestationCertifiedDevice property"""
        return self.properties.get("securityRequireSafetyNetAttestationCertifiedDevice", None)

    @odata(name="securityRequireUpToDateSecurityProviders")
    @property
    def security_require_up_to_date_security_providers(self) -> Optional[bool]:
        """Gets the securityRequireUpToDateSecurityProviders property"""
        return self.properties.get("securityRequireUpToDateSecurityProviders", None)

    @odata(name="securityRequireVerifyApps")
    @property
    def security_require_verify_apps(self) -> Optional[bool]:
        """Gets the securityRequireVerifyApps property"""
        return self.properties.get("securityRequireVerifyApps", None)

    @odata(name="storageRequireEncryption")
    @property
    def storage_require_encryption(self) -> Optional[bool]:
        """Gets the storageRequireEncryption property"""
        return self.properties.get("storageRequireEncryption", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidWorkProfileCompliancePolicy"
