from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.androidrequiredpasswordtype import (
        AndroidRequiredPasswordType,
    )
    from office365.intune.devices.configurations.applisttype import AppListType
    from office365.intune.devices.configurations.webbrowsercookiesettings import (
        WebBrowserCookieSettings,
    )
    from office365.intune.devices.management.mobileapps.app_list_item import AppListItem


class AndroidGeneralDeviceConfiguration(Entity):
    @odata(name="appsBlockClipboardSharing")
    @property
    def apps_block_clipboard_sharing(self) -> Optional[bool]:
        """Gets the appsBlockClipboardSharing property"""
        return self.properties.get("appsBlockClipboardSharing", None)

    @odata(name="appsBlockCopyPaste")
    @property
    def apps_block_copy_paste(self) -> Optional[bool]:
        """Gets the appsBlockCopyPaste property"""
        return self.properties.get("appsBlockCopyPaste", None)

    @odata(name="appsBlockYouTube")
    @property
    def apps_block_you_tube(self) -> Optional[bool]:
        """Gets the appsBlockYouTube property"""
        return self.properties.get("appsBlockYouTube", None)

    @odata(name="appsHideList")
    @property
    def apps_hide_list(self) -> ClientValueCollection[AppListItem]:
        """Gets the appsHideList property"""
        from office365.intune.devices.management.mobileapps.app_list_item import AppListItem

        return self.properties.get("appsHideList", ClientValueCollection[AppListItem](AppListItem))

    @odata(name="appsInstallAllowList")
    @property
    def apps_install_allow_list(self) -> ClientValueCollection[AppListItem]:
        """Gets the appsInstallAllowList property"""
        from office365.intune.devices.management.mobileapps.app_list_item import AppListItem

        return self.properties.get("appsInstallAllowList", ClientValueCollection[AppListItem](AppListItem))

    @odata(name="appsLaunchBlockList")
    @property
    def apps_launch_block_list(self) -> ClientValueCollection[AppListItem]:
        """Gets the appsLaunchBlockList property"""
        from office365.intune.devices.management.mobileapps.app_list_item import AppListItem

        return self.properties.get("appsLaunchBlockList", ClientValueCollection[AppListItem](AppListItem))

    @odata(name="bluetoothBlocked")
    @property
    def bluetooth_blocked(self) -> Optional[bool]:
        """Gets the bluetoothBlocked property"""
        return self.properties.get("bluetoothBlocked", None)

    @odata(name="cameraBlocked")
    @property
    def camera_blocked(self) -> Optional[bool]:
        """Gets the cameraBlocked property"""
        return self.properties.get("cameraBlocked", None)

    @odata(name="cellularBlockDataRoaming")
    @property
    def cellular_block_data_roaming(self) -> Optional[bool]:
        """Gets the cellularBlockDataRoaming property"""
        return self.properties.get("cellularBlockDataRoaming", None)

    @odata(name="cellularBlockMessaging")
    @property
    def cellular_block_messaging(self) -> Optional[bool]:
        """Gets the cellularBlockMessaging property"""
        return self.properties.get("cellularBlockMessaging", None)

    @odata(name="cellularBlockVoiceRoaming")
    @property
    def cellular_block_voice_roaming(self) -> Optional[bool]:
        """Gets the cellularBlockVoiceRoaming property"""
        return self.properties.get("cellularBlockVoiceRoaming", None)

    @odata(name="cellularBlockWiFiTethering")
    @property
    def cellular_block_wi_fi_tethering(self) -> Optional[bool]:
        """Gets the cellularBlockWiFiTethering property"""
        return self.properties.get("cellularBlockWiFiTethering", None)

    @odata(name="compliantAppListType")
    @property
    def compliant_app_list_type(self) -> AppListType:
        """Gets the compliantAppListType property"""
        from office365.intune.devices.configurations.applisttype import AppListType

        return self.properties.get("compliantAppListType", AppListType.none)

    @odata(name="compliantAppsList")
    @property
    def compliant_apps_list(self) -> ClientValueCollection[AppListItem]:
        """Gets the compliantAppsList property"""
        from office365.intune.devices.management.mobileapps.app_list_item import AppListItem

        return self.properties.get("compliantAppsList", ClientValueCollection[AppListItem](AppListItem))

    @odata(name="deviceSharingAllowed")
    @property
    def device_sharing_allowed(self) -> Optional[bool]:
        """Gets the deviceSharingAllowed property"""
        return self.properties.get("deviceSharingAllowed", None)

    @odata(name="diagnosticDataBlockSubmission")
    @property
    def diagnostic_data_block_submission(self) -> Optional[bool]:
        """Gets the diagnosticDataBlockSubmission property"""
        return self.properties.get("diagnosticDataBlockSubmission", None)

    @odata(name="factoryResetBlocked")
    @property
    def factory_reset_blocked(self) -> Optional[bool]:
        """Gets the factoryResetBlocked property"""
        return self.properties.get("factoryResetBlocked", None)

    @odata(name="googleAccountBlockAutoSync")
    @property
    def google_account_block_auto_sync(self) -> Optional[bool]:
        """Gets the googleAccountBlockAutoSync property"""
        return self.properties.get("googleAccountBlockAutoSync", None)

    @odata(name="googlePlayStoreBlocked")
    @property
    def google_play_store_blocked(self) -> Optional[bool]:
        """Gets the googlePlayStoreBlocked property"""
        return self.properties.get("googlePlayStoreBlocked", None)

    @odata(name="kioskModeApps")
    @property
    def kiosk_mode_apps(self) -> ClientValueCollection[AppListItem]:
        """Gets the kioskModeApps property"""
        from office365.intune.devices.management.mobileapps.app_list_item import AppListItem

        return self.properties.get("kioskModeApps", ClientValueCollection[AppListItem](AppListItem))

    @odata(name="kioskModeBlockSleepButton")
    @property
    def kiosk_mode_block_sleep_button(self) -> Optional[bool]:
        """Gets the kioskModeBlockSleepButton property"""
        return self.properties.get("kioskModeBlockSleepButton", None)

    @odata(name="kioskModeBlockVolumeButtons")
    @property
    def kiosk_mode_block_volume_buttons(self) -> Optional[bool]:
        """Gets the kioskModeBlockVolumeButtons property"""
        return self.properties.get("kioskModeBlockVolumeButtons", None)

    @odata(name="locationServicesBlocked")
    @property
    def location_services_blocked(self) -> Optional[bool]:
        """Gets the locationServicesBlocked property"""
        return self.properties.get("locationServicesBlocked", None)

    @odata(name="nfcBlocked")
    @property
    def nfc_blocked(self) -> Optional[bool]:
        """Gets the nfcBlocked property"""
        return self.properties.get("nfcBlocked", None)

    @odata(name="passwordBlockFingerprintUnlock")
    @property
    def password_block_fingerprint_unlock(self) -> Optional[bool]:
        """Gets the passwordBlockFingerprintUnlock property"""
        return self.properties.get("passwordBlockFingerprintUnlock", None)

    @odata(name="passwordBlockTrustAgents")
    @property
    def password_block_trust_agents(self) -> Optional[bool]:
        """Gets the passwordBlockTrustAgents property"""
        return self.properties.get("passwordBlockTrustAgents", None)

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

    @odata(name="passwordMinutesOfInactivityBeforeScreenTimeout")
    @property
    def password_minutes_of_inactivity_before_screen_timeout(self) -> Optional[int]:
        """Gets the passwordMinutesOfInactivityBeforeScreenTimeout property"""
        return self.properties.get("passwordMinutesOfInactivityBeforeScreenTimeout", None)

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

    @odata(name="passwordSignInFailureCountBeforeFactoryReset")
    @property
    def password_sign_in_failure_count_before_factory_reset(self) -> Optional[int]:
        """Gets the passwordSignInFailureCountBeforeFactoryReset property"""
        return self.properties.get("passwordSignInFailureCountBeforeFactoryReset", None)

    @odata(name="powerOffBlocked")
    @property
    def power_off_blocked(self) -> Optional[bool]:
        """Gets the powerOffBlocked property"""
        return self.properties.get("powerOffBlocked", None)

    @odata(name="screenCaptureBlocked")
    @property
    def screen_capture_blocked(self) -> Optional[bool]:
        """Gets the screenCaptureBlocked property"""
        return self.properties.get("screenCaptureBlocked", None)

    @odata(name="securityRequireVerifyApps")
    @property
    def security_require_verify_apps(self) -> Optional[bool]:
        """Gets the securityRequireVerifyApps property"""
        return self.properties.get("securityRequireVerifyApps", None)

    @odata(name="storageBlockGoogleBackup")
    @property
    def storage_block_google_backup(self) -> Optional[bool]:
        """Gets the storageBlockGoogleBackup property"""
        return self.properties.get("storageBlockGoogleBackup", None)

    @odata(name="storageBlockRemovableStorage")
    @property
    def storage_block_removable_storage(self) -> Optional[bool]:
        """Gets the storageBlockRemovableStorage property"""
        return self.properties.get("storageBlockRemovableStorage", None)

    @odata(name="storageRequireDeviceEncryption")
    @property
    def storage_require_device_encryption(self) -> Optional[bool]:
        """Gets the storageRequireDeviceEncryption property"""
        return self.properties.get("storageRequireDeviceEncryption", None)

    @odata(name="storageRequireRemovableStorageEncryption")
    @property
    def storage_require_removable_storage_encryption(self) -> Optional[bool]:
        """Gets the storageRequireRemovableStorageEncryption property"""
        return self.properties.get("storageRequireRemovableStorageEncryption", None)

    @odata(name="voiceAssistantBlocked")
    @property
    def voice_assistant_blocked(self) -> Optional[bool]:
        """Gets the voiceAssistantBlocked property"""
        return self.properties.get("voiceAssistantBlocked", None)

    @odata(name="voiceDialingBlocked")
    @property
    def voice_dialing_blocked(self) -> Optional[bool]:
        """Gets the voiceDialingBlocked property"""
        return self.properties.get("voiceDialingBlocked", None)

    @odata(name="webBrowserBlockAutofill")
    @property
    def web_browser_block_autofill(self) -> Optional[bool]:
        """Gets the webBrowserBlockAutofill property"""
        return self.properties.get("webBrowserBlockAutofill", None)

    @odata(name="webBrowserBlocked")
    @property
    def web_browser_blocked(self) -> Optional[bool]:
        """Gets the webBrowserBlocked property"""
        return self.properties.get("webBrowserBlocked", None)

    @odata(name="webBrowserBlockJavaScript")
    @property
    def web_browser_block_java_script(self) -> Optional[bool]:
        """Gets the webBrowserBlockJavaScript property"""
        return self.properties.get("webBrowserBlockJavaScript", None)

    @odata(name="webBrowserBlockPopups")
    @property
    def web_browser_block_popups(self) -> Optional[bool]:
        """Gets the webBrowserBlockPopups property"""
        return self.properties.get("webBrowserBlockPopups", None)

    @odata(name="webBrowserCookieSettings")
    @property
    def web_browser_cookie_settings(self) -> WebBrowserCookieSettings:
        """Gets the webBrowserCookieSettings property"""
        from office365.intune.devices.configurations.webbrowsercookiesettings import (
            WebBrowserCookieSettings,
        )

        return self.properties.get("webBrowserCookieSettings", WebBrowserCookieSettings.browserDefault)

    @odata(name="wiFiBlocked")
    @property
    def wi_fi_blocked(self) -> Optional[bool]:
        """Gets the wiFiBlocked property"""
        return self.properties.get("wiFiBlocked", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidGeneralDeviceConfiguration"
