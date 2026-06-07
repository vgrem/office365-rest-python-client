from __future__ import annotations

from datetime import timedelta
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.managed.app.clipboardsharinglevel import ManagedAppClipboardSharingLevel
from office365.intune.devices.management.managed.app.datastoragelocation import ManagedAppDataStorageLocation
from office365.intune.devices.management.managed.app.datatransferlevel import ManagedAppDataTransferLevel
from office365.intune.devices.management.managed.app.managedbrowsertype import ManagedBrowserType
from office365.intune.devices.management.managed.app.pincharacterset import ManagedAppPinCharacterSet
from office365.runtime.client_value_collection import ClientValueCollection


class ManagedAppProtection(Entity):
    @property
    def allowed_data_storage_locations(self) -> ClientValueCollection[ManagedAppDataStorageLocation]:
        """Gets the allowedDataStorageLocations property"""
        return self.properties.get(
            "allowedDataStorageLocations",
            ClientValueCollection[ManagedAppDataStorageLocation](ManagedAppDataStorageLocation),
        )

    @property
    def allowed_inbound_data_transfer_sources(self) -> ManagedAppDataTransferLevel:
        """Gets the allowedInboundDataTransferSources property"""
        return self.properties.get("allowedInboundDataTransferSources", ManagedAppDataTransferLevel.allApps)

    @property
    def allowed_outbound_clipboard_sharing_level(self) -> ManagedAppClipboardSharingLevel:
        """Gets the allowedOutboundClipboardSharingLevel property"""
        return self.properties.get("allowedOutboundClipboardSharingLevel", ManagedAppClipboardSharingLevel.allApps)

    @property
    def allowed_outbound_data_transfer_destinations(self) -> ManagedAppDataTransferLevel:
        """Gets the allowedOutboundDataTransferDestinations property"""
        return self.properties.get("allowedOutboundDataTransferDestinations", ManagedAppDataTransferLevel.allApps)

    @property
    def contact_sync_blocked(self) -> Optional[bool]:
        """Gets the contactSyncBlocked property"""
        return self.properties.get("contactSyncBlocked", None)

    @property
    def data_backup_blocked(self) -> Optional[bool]:
        """Gets the dataBackupBlocked property"""
        return self.properties.get("dataBackupBlocked", None)

    @property
    def device_compliance_required(self) -> Optional[bool]:
        """Gets the deviceComplianceRequired property"""
        return self.properties.get("deviceComplianceRequired", None)

    @property
    def disable_app_pin_if_device_pin_is_set(self) -> Optional[bool]:
        """Gets the disableAppPinIfDevicePinIsSet property"""
        return self.properties.get("disableAppPinIfDevicePinIsSet", None)

    @property
    def fingerprint_blocked(self) -> Optional[bool]:
        """Gets the fingerprintBlocked property"""
        return self.properties.get("fingerprintBlocked", None)

    @property
    def managed_browser(self) -> ManagedBrowserType:
        """Gets the managedBrowser property"""
        return self.properties.get("managedBrowser", ManagedBrowserType.notConfigured)

    @property
    def managed_browser_to_open_links_required(self) -> Optional[bool]:
        """Gets the managedBrowserToOpenLinksRequired property"""
        return self.properties.get("managedBrowserToOpenLinksRequired", None)

    @property
    def maximum_pin_retries(self) -> Optional[int]:
        """Gets the maximumPinRetries property"""
        return self.properties.get("maximumPinRetries", None)

    @property
    def minimum_pin_length(self) -> Optional[int]:
        """Gets the minimumPinLength property"""
        return self.properties.get("minimumPinLength", None)

    @property
    def minimum_required_app_version(self) -> Optional[str]:
        """Gets the minimumRequiredAppVersion property"""
        return self.properties.get("minimumRequiredAppVersion", None)

    @property
    def minimum_required_os_version(self) -> Optional[str]:
        """Gets the minimumRequiredOsVersion property"""
        return self.properties.get("minimumRequiredOsVersion", None)

    @property
    def minimum_warning_app_version(self) -> Optional[str]:
        """Gets the minimumWarningAppVersion property"""
        return self.properties.get("minimumWarningAppVersion", None)

    @property
    def minimum_warning_os_version(self) -> Optional[str]:
        """Gets the minimumWarningOsVersion property"""
        return self.properties.get("minimumWarningOsVersion", None)

    @property
    def organizational_credentials_required(self) -> Optional[bool]:
        """Gets the organizationalCredentialsRequired property"""
        return self.properties.get("organizationalCredentialsRequired", None)

    @property
    def period_before_pin_reset(self) -> timedelta:
        """Gets the periodBeforePinReset property"""
        return self.properties.get("periodBeforePinReset", timedelta.min)

    @property
    def period_offline_before_access_check(self) -> timedelta:
        """Gets the periodOfflineBeforeAccessCheck property"""
        return self.properties.get("periodOfflineBeforeAccessCheck", timedelta.min)

    @property
    def period_offline_before_wipe_is_enforced(self) -> timedelta:
        """Gets the periodOfflineBeforeWipeIsEnforced property"""
        return self.properties.get("periodOfflineBeforeWipeIsEnforced", timedelta.min)

    @property
    def period_online_before_access_check(self) -> timedelta:
        """Gets the periodOnlineBeforeAccessCheck property"""
        return self.properties.get("periodOnlineBeforeAccessCheck", timedelta.min)

    @property
    def pin_character_set(self) -> ManagedAppPinCharacterSet:
        """Gets the pinCharacterSet property"""
        return self.properties.get("pinCharacterSet", ManagedAppPinCharacterSet.numeric)

    @property
    def pin_required(self) -> Optional[bool]:
        """Gets the pinRequired property"""
        return self.properties.get("pinRequired", None)

    @property
    def print_blocked(self) -> Optional[bool]:
        """Gets the printBlocked property"""
        return self.properties.get("printBlocked", None)

    @property
    def save_as_blocked(self) -> Optional[bool]:
        """Gets the saveAsBlocked property"""
        return self.properties.get("saveAsBlocked", None)

    @property
    def simple_pin_blocked(self) -> Optional[bool]:
        """Gets the simplePinBlocked property"""
        return self.properties.get("simplePinBlocked", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAppProtection"
