from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.windows_information_protection_pin_character_requirements import (
        WindowsInformationProtectionPinCharacterRequirements,
    )


class WindowsInformationProtectionPolicy(Entity):
    @odata(name="daysWithoutContactBeforeUnenroll")
    @property
    def days_without_contact_before_unenroll(self) -> Optional[int]:
        """Gets the daysWithoutContactBeforeUnenroll property"""
        return self.properties.get("daysWithoutContactBeforeUnenroll", None)

    @odata(name="mdmEnrollmentUrl")
    @property
    def mdm_enrollment_url(self) -> Optional[str]:
        """Gets the mdmEnrollmentUrl property"""
        return self.properties.get("mdmEnrollmentUrl", None)

    @odata(name="minutesOfInactivityBeforeDeviceLock")
    @property
    def minutes_of_inactivity_before_device_lock(self) -> Optional[int]:
        """Gets the minutesOfInactivityBeforeDeviceLock property"""
        return self.properties.get("minutesOfInactivityBeforeDeviceLock", None)

    @odata(name="numberOfPastPinsRemembered")
    @property
    def number_of_past_pins_remembered(self) -> Optional[int]:
        """Gets the numberOfPastPinsRemembered property"""
        return self.properties.get("numberOfPastPinsRemembered", None)

    @odata(name="passwordMaximumAttemptCount")
    @property
    def password_maximum_attempt_count(self) -> Optional[int]:
        """Gets the passwordMaximumAttemptCount property"""
        return self.properties.get("passwordMaximumAttemptCount", None)

    @odata(name="pinExpirationDays")
    @property
    def pin_expiration_days(self) -> Optional[int]:
        """Gets the pinExpirationDays property"""
        return self.properties.get("pinExpirationDays", None)

    @odata(name="pinLowercaseLetters")
    @property
    def pin_lowercase_letters(self) -> Optional[WindowsInformationProtectionPinCharacterRequirements]:
        """Gets the pinLowercaseLetters property"""
        return self.properties.get("pinLowercaseLetters", None)

    @odata(name="pinMinimumLength")
    @property
    def pin_minimum_length(self) -> Optional[int]:
        """Gets the pinMinimumLength property"""
        return self.properties.get("pinMinimumLength", None)

    @odata(name="pinSpecialCharacters")
    @property
    def pin_special_characters(self) -> Optional[WindowsInformationProtectionPinCharacterRequirements]:
        """Gets the pinSpecialCharacters property"""
        return self.properties.get("pinSpecialCharacters", None)

    @odata(name="pinUppercaseLetters")
    @property
    def pin_uppercase_letters(self) -> Optional[WindowsInformationProtectionPinCharacterRequirements]:
        """Gets the pinUppercaseLetters property"""
        return self.properties.get("pinUppercaseLetters", None)

    @odata(name="revokeOnMdmHandoffDisabled")
    @property
    def revoke_on_mdm_handoff_disabled(self) -> Optional[bool]:
        """Gets the revokeOnMdmHandoffDisabled property"""
        return self.properties.get("revokeOnMdmHandoffDisabled", None)

    @odata(name="windowsHelloForBusinessBlocked")
    @property
    def windows_hello_for_business_blocked(self) -> Optional[bool]:
        """Gets the windowsHelloForBusinessBlocked property"""
        return self.properties.get("windowsHelloForBusinessBlocked", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionPolicy"
