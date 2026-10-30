from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.configurations.enablement import Enablement
    from office365.intune.devices.configurations.windows.helloforbusinesspinusage import (
        WindowsHelloForBusinessPinUsage,
    )


class DeviceEnrollmentWindowsHelloForBusinessConfiguration(Entity):
    @odata(name="enhancedBiometricsState")
    @property
    def enhanced_biometrics_state(self) -> Enablement:
        """Gets the enhancedBiometricsState property"""
        from office365.intune.devices.configurations.enablement import Enablement

        return self.properties.get("enhancedBiometricsState", Enablement.notConfigured)

    @odata(name="pinExpirationInDays")
    @property
    def pin_expiration_in_days(self) -> Optional[int]:
        """Gets the pinExpirationInDays property"""
        return self.properties.get("pinExpirationInDays", None)

    @odata(name="pinLowercaseCharactersUsage")
    @property
    def pin_lowercase_characters_usage(self) -> WindowsHelloForBusinessPinUsage:
        """Gets the pinLowercaseCharactersUsage property"""
        from office365.intune.devices.configurations.windows.helloforbusinesspinusage import (
            WindowsHelloForBusinessPinUsage,
        )

        return self.properties.get("pinLowercaseCharactersUsage", WindowsHelloForBusinessPinUsage.allowed)

    @odata(name="pinMaximumLength")
    @property
    def pin_maximum_length(self) -> Optional[int]:
        """Gets the pinMaximumLength property"""
        return self.properties.get("pinMaximumLength", None)

    @odata(name="pinMinimumLength")
    @property
    def pin_minimum_length(self) -> Optional[int]:
        """Gets the pinMinimumLength property"""
        return self.properties.get("pinMinimumLength", None)

    @odata(name="pinPreviousBlockCount")
    @property
    def pin_previous_block_count(self) -> Optional[int]:
        """Gets the pinPreviousBlockCount property"""
        return self.properties.get("pinPreviousBlockCount", None)

    @odata(name="pinSpecialCharactersUsage")
    @property
    def pin_special_characters_usage(self) -> WindowsHelloForBusinessPinUsage:
        """Gets the pinSpecialCharactersUsage property"""
        from office365.intune.devices.configurations.windows.helloforbusinesspinusage import (
            WindowsHelloForBusinessPinUsage,
        )

        return self.properties.get("pinSpecialCharactersUsage", WindowsHelloForBusinessPinUsage.allowed)

    @odata(name="pinUppercaseCharactersUsage")
    @property
    def pin_uppercase_characters_usage(self) -> WindowsHelloForBusinessPinUsage:
        """Gets the pinUppercaseCharactersUsage property"""
        from office365.intune.devices.configurations.windows.helloforbusinesspinusage import (
            WindowsHelloForBusinessPinUsage,
        )

        return self.properties.get("pinUppercaseCharactersUsage", WindowsHelloForBusinessPinUsage.allowed)

    @odata(name="remotePassportEnabled")
    @property
    def remote_passport_enabled(self) -> Optional[bool]:
        """Gets the remotePassportEnabled property"""
        return self.properties.get("remotePassportEnabled", None)

    @odata(name="securityDeviceRequired")
    @property
    def security_device_required(self) -> Optional[bool]:
        """Gets the securityDeviceRequired property"""
        return self.properties.get("securityDeviceRequired", None)

    @odata(name="state")
    @property
    def state(self) -> Enablement:
        """Gets the state property"""
        from office365.intune.devices.configurations.enablement import Enablement

        return self.properties.get("state", Enablement.notConfigured)

    @odata(name="unlockWithBiometricsEnabled")
    @property
    def unlock_with_biometrics_enabled(self) -> Optional[bool]:
        """Gets the unlockWithBiometricsEnabled property"""
        return self.properties.get("unlockWithBiometricsEnabled", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceEnrollmentWindowsHelloForBusinessConfiguration"
