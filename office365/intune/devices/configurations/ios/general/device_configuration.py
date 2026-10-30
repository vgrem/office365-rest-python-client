from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.requiredpasswordtype import RequiredPasswordType
from office365.intune.devices.configurations.applisttype import AppListType
from office365.intune.devices.configurations.ios.general.ratingappstype import RatingAppsType
from office365.intune.devices.configurations.ios.network_usage_rule import IosNetworkUsageRule
from office365.intune.devices.configurations.media_content_rating_australia import MediaContentRatingAustralia
from office365.intune.devices.configurations.media_content_rating_canada import MediaContentRatingCanada
from office365.intune.devices.configurations.media_content_rating_france import MediaContentRatingFrance
from office365.intune.devices.configurations.media_content_rating_germany import MediaContentRatingGermany
from office365.intune.devices.configurations.media_content_rating_ireland import MediaContentRatingIreland
from office365.intune.devices.configurations.media_content_rating_japan import MediaContentRatingJapan
from office365.intune.devices.configurations.media_content_rating_new_zealand import MediaContentRatingNewZealand
from office365.intune.devices.configurations.media_content_rating_united_kingdom import MediaContentRatingUnitedKingdom
from office365.intune.devices.configurations.media_content_rating_united_states import MediaContentRatingUnitedStates
from office365.intune.devices.configurations.webbrowsercookiesettings import WebBrowserCookieSettings
from office365.intune.devices.management.mobileapps.app_list_item import AppListItem
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class IosGeneralDeviceConfiguration(Entity):
    @odata(name="accountBlockModification")
    @property
    def account_block_modification(self) -> Optional[bool]:
        """Gets the accountBlockModification property"""
        return self.properties.get("accountBlockModification", None)

    @odata(name="activationLockAllowWhenSupervised")
    @property
    def activation_lock_allow_when_supervised(self) -> Optional[bool]:
        """Gets the activationLockAllowWhenSupervised property"""
        return self.properties.get("activationLockAllowWhenSupervised", None)

    @odata(name="airDropBlocked")
    @property
    def air_drop_blocked(self) -> Optional[bool]:
        """Gets the airDropBlocked property"""
        return self.properties.get("airDropBlocked", None)

    @odata(name="airDropForceUnmanagedDropTarget")
    @property
    def air_drop_force_unmanaged_drop_target(self) -> Optional[bool]:
        """Gets the airDropForceUnmanagedDropTarget property"""
        return self.properties.get("airDropForceUnmanagedDropTarget", None)

    @odata(name="airPlayForcePairingPasswordForOutgoingRequests")
    @property
    def air_play_force_pairing_password_for_outgoing_requests(self) -> Optional[bool]:
        """Gets the airPlayForcePairingPasswordForOutgoingRequests property"""
        return self.properties.get("airPlayForcePairingPasswordForOutgoingRequests", None)

    @odata(name="appleNewsBlocked")
    @property
    def apple_news_blocked(self) -> Optional[bool]:
        """Gets the appleNewsBlocked property"""
        return self.properties.get("appleNewsBlocked", None)

    @odata(name="appleWatchBlockPairing")
    @property
    def apple_watch_block_pairing(self) -> Optional[bool]:
        """Gets the appleWatchBlockPairing property"""
        return self.properties.get("appleWatchBlockPairing", None)

    @odata(name="appleWatchForceWristDetection")
    @property
    def apple_watch_force_wrist_detection(self) -> Optional[bool]:
        """Gets the appleWatchForceWristDetection property"""
        return self.properties.get("appleWatchForceWristDetection", None)

    @odata(name="appsSingleAppModeList")
    @property
    def apps_single_app_mode_list(self) -> ClientValueCollection[AppListItem]:
        """Gets the appsSingleAppModeList property"""
        return self.properties.get("appsSingleAppModeList", ClientValueCollection[AppListItem](AppListItem))

    @odata(name="appStoreBlockAutomaticDownloads")
    @property
    def app_store_block_automatic_downloads(self) -> Optional[bool]:
        """Gets the appStoreBlockAutomaticDownloads property"""
        return self.properties.get("appStoreBlockAutomaticDownloads", None)

    @odata(name="appStoreBlocked")
    @property
    def app_store_blocked(self) -> Optional[bool]:
        """Gets the appStoreBlocked property"""
        return self.properties.get("appStoreBlocked", None)

    @odata(name="appStoreBlockInAppPurchases")
    @property
    def app_store_block_in_app_purchases(self) -> Optional[bool]:
        """Gets the appStoreBlockInAppPurchases property"""
        return self.properties.get("appStoreBlockInAppPurchases", None)

    @odata(name="appStoreBlockUIAppInstallation")
    @property
    def app_store_block_ui_app_installation(self) -> Optional[bool]:
        """Gets the appStoreBlockUIAppInstallation property"""
        return self.properties.get("appStoreBlockUIAppInstallation", None)

    @odata(name="appStoreRequirePassword")
    @property
    def app_store_require_password(self) -> Optional[bool]:
        """Gets the appStoreRequirePassword property"""
        return self.properties.get("appStoreRequirePassword", None)

    @odata(name="appsVisibilityList")
    @property
    def apps_visibility_list(self) -> ClientValueCollection[AppListItem]:
        """Gets the appsVisibilityList property"""
        return self.properties.get("appsVisibilityList", ClientValueCollection[AppListItem](AppListItem))

    @odata(name="appsVisibilityListType")
    @property
    def apps_visibility_list_type(self) -> AppListType:
        """Gets the appsVisibilityListType property"""
        return self.properties.get("appsVisibilityListType", AppListType.none)

    @odata(name="bluetoothBlockModification")
    @property
    def bluetooth_block_modification(self) -> Optional[bool]:
        """Gets the bluetoothBlockModification property"""
        return self.properties.get("bluetoothBlockModification", None)

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

    @odata(name="cellularBlockGlobalBackgroundFetchWhileRoaming")
    @property
    def cellular_block_global_background_fetch_while_roaming(self) -> Optional[bool]:
        """Gets the cellularBlockGlobalBackgroundFetchWhileRoaming property"""
        return self.properties.get("cellularBlockGlobalBackgroundFetchWhileRoaming", None)

    @odata(name="cellularBlockPerAppDataModification")
    @property
    def cellular_block_per_app_data_modification(self) -> Optional[bool]:
        """Gets the cellularBlockPerAppDataModification property"""
        return self.properties.get("cellularBlockPerAppDataModification", None)

    @odata(name="cellularBlockPersonalHotspot")
    @property
    def cellular_block_personal_hotspot(self) -> Optional[bool]:
        """Gets the cellularBlockPersonalHotspot property"""
        return self.properties.get("cellularBlockPersonalHotspot", None)

    @odata(name="cellularBlockVoiceRoaming")
    @property
    def cellular_block_voice_roaming(self) -> Optional[bool]:
        """Gets the cellularBlockVoiceRoaming property"""
        return self.properties.get("cellularBlockVoiceRoaming", None)

    @odata(name="certificatesBlockUntrustedTlsCertificates")
    @property
    def certificates_block_untrusted_tls_certificates(self) -> Optional[bool]:
        """Gets the certificatesBlockUntrustedTlsCertificates property"""
        return self.properties.get("certificatesBlockUntrustedTlsCertificates", None)

    @odata(name="classroomAppBlockRemoteScreenObservation")
    @property
    def classroom_app_block_remote_screen_observation(self) -> Optional[bool]:
        """Gets the classroomAppBlockRemoteScreenObservation property"""
        return self.properties.get("classroomAppBlockRemoteScreenObservation", None)

    @odata(name="classroomAppForceUnpromptedScreenObservation")
    @property
    def classroom_app_force_unprompted_screen_observation(self) -> Optional[bool]:
        """Gets the classroomAppForceUnpromptedScreenObservation property"""
        return self.properties.get("classroomAppForceUnpromptedScreenObservation", None)

    @odata(name="compliantAppListType")
    @property
    def compliant_app_list_type(self) -> AppListType:
        """Gets the compliantAppListType property"""
        return self.properties.get("compliantAppListType", AppListType.none)

    @odata(name="compliantAppsList")
    @property
    def compliant_apps_list(self) -> ClientValueCollection[AppListItem]:
        """Gets the compliantAppsList property"""
        return self.properties.get("compliantAppsList", ClientValueCollection[AppListItem](AppListItem))

    @odata(name="configurationProfileBlockChanges")
    @property
    def configuration_profile_block_changes(self) -> Optional[bool]:
        """Gets the configurationProfileBlockChanges property"""
        return self.properties.get("configurationProfileBlockChanges", None)

    @odata(name="definitionLookupBlocked")
    @property
    def definition_lookup_blocked(self) -> Optional[bool]:
        """Gets the definitionLookupBlocked property"""
        return self.properties.get("definitionLookupBlocked", None)

    @odata(name="deviceBlockEnableRestrictions")
    @property
    def device_block_enable_restrictions(self) -> Optional[bool]:
        """Gets the deviceBlockEnableRestrictions property"""
        return self.properties.get("deviceBlockEnableRestrictions", None)

    @odata(name="deviceBlockEraseContentAndSettings")
    @property
    def device_block_erase_content_and_settings(self) -> Optional[bool]:
        """Gets the deviceBlockEraseContentAndSettings property"""
        return self.properties.get("deviceBlockEraseContentAndSettings", None)

    @odata(name="deviceBlockNameModification")
    @property
    def device_block_name_modification(self) -> Optional[bool]:
        """Gets the deviceBlockNameModification property"""
        return self.properties.get("deviceBlockNameModification", None)

    @odata(name="diagnosticDataBlockSubmission")
    @property
    def diagnostic_data_block_submission(self) -> Optional[bool]:
        """Gets the diagnosticDataBlockSubmission property"""
        return self.properties.get("diagnosticDataBlockSubmission", None)

    @odata(name="diagnosticDataBlockSubmissionModification")
    @property
    def diagnostic_data_block_submission_modification(self) -> Optional[bool]:
        """Gets the diagnosticDataBlockSubmissionModification property"""
        return self.properties.get("diagnosticDataBlockSubmissionModification", None)

    @odata(name="documentsBlockManagedDocumentsInUnmanagedApps")
    @property
    def documents_block_managed_documents_in_unmanaged_apps(self) -> Optional[bool]:
        """Gets the documentsBlockManagedDocumentsInUnmanagedApps property"""
        return self.properties.get("documentsBlockManagedDocumentsInUnmanagedApps", None)

    @odata(name="documentsBlockUnmanagedDocumentsInManagedApps")
    @property
    def documents_block_unmanaged_documents_in_managed_apps(self) -> Optional[bool]:
        """Gets the documentsBlockUnmanagedDocumentsInManagedApps property"""
        return self.properties.get("documentsBlockUnmanagedDocumentsInManagedApps", None)

    @odata(name="emailInDomainSuffixes")
    @property
    def email_in_domain_suffixes(self) -> StringCollection:
        """Gets the emailInDomainSuffixes property"""
        return self.properties.get("emailInDomainSuffixes", StringCollection())

    @odata(name="enterpriseAppBlockTrust")
    @property
    def enterprise_app_block_trust(self) -> Optional[bool]:
        """Gets the enterpriseAppBlockTrust property"""
        return self.properties.get("enterpriseAppBlockTrust", None)

    @odata(name="enterpriseAppBlockTrustModification")
    @property
    def enterprise_app_block_trust_modification(self) -> Optional[bool]:
        """Gets the enterpriseAppBlockTrustModification property"""
        return self.properties.get("enterpriseAppBlockTrustModification", None)

    @odata(name="faceTimeBlocked")
    @property
    def face_time_blocked(self) -> Optional[bool]:
        """Gets the faceTimeBlocked property"""
        return self.properties.get("faceTimeBlocked", None)

    @odata(name="findMyFriendsBlocked")
    @property
    def find_my_friends_blocked(self) -> Optional[bool]:
        """Gets the findMyFriendsBlocked property"""
        return self.properties.get("findMyFriendsBlocked", None)

    @odata(name="gameCenterBlocked")
    @property
    def game_center_blocked(self) -> Optional[bool]:
        """Gets the gameCenterBlocked property"""
        return self.properties.get("gameCenterBlocked", None)

    @odata(name="gamingBlockGameCenterFriends")
    @property
    def gaming_block_game_center_friends(self) -> Optional[bool]:
        """Gets the gamingBlockGameCenterFriends property"""
        return self.properties.get("gamingBlockGameCenterFriends", None)

    @odata(name="gamingBlockMultiplayer")
    @property
    def gaming_block_multiplayer(self) -> Optional[bool]:
        """Gets the gamingBlockMultiplayer property"""
        return self.properties.get("gamingBlockMultiplayer", None)

    @odata(name="hostPairingBlocked")
    @property
    def host_pairing_blocked(self) -> Optional[bool]:
        """Gets the hostPairingBlocked property"""
        return self.properties.get("hostPairingBlocked", None)

    @odata(name="iBooksStoreBlocked")
    @property
    def ibooks_store_blocked(self) -> Optional[bool]:
        """Gets the iBooksStoreBlocked property"""
        return self.properties.get("iBooksStoreBlocked", None)

    @odata(name="iBooksStoreBlockErotica")
    @property
    def ibooks_store_block_erotica(self) -> Optional[bool]:
        """Gets the iBooksStoreBlockErotica property"""
        return self.properties.get("iBooksStoreBlockErotica", None)

    @odata(name="iCloudBlockActivityContinuation")
    @property
    def icloud_block_activity_continuation(self) -> Optional[bool]:
        """Gets the iCloudBlockActivityContinuation property"""
        return self.properties.get("iCloudBlockActivityContinuation", None)

    @odata(name="iCloudBlockBackup")
    @property
    def icloud_block_backup(self) -> Optional[bool]:
        """Gets the iCloudBlockBackup property"""
        return self.properties.get("iCloudBlockBackup", None)

    @odata(name="iCloudBlockDocumentSync")
    @property
    def icloud_block_document_sync(self) -> Optional[bool]:
        """Gets the iCloudBlockDocumentSync property"""
        return self.properties.get("iCloudBlockDocumentSync", None)

    @odata(name="iCloudBlockManagedAppsSync")
    @property
    def icloud_block_managed_apps_sync(self) -> Optional[bool]:
        """Gets the iCloudBlockManagedAppsSync property"""
        return self.properties.get("iCloudBlockManagedAppsSync", None)

    @odata(name="iCloudBlockPhotoLibrary")
    @property
    def icloud_block_photo_library(self) -> Optional[bool]:
        """Gets the iCloudBlockPhotoLibrary property"""
        return self.properties.get("iCloudBlockPhotoLibrary", None)

    @odata(name="iCloudBlockPhotoStreamSync")
    @property
    def icloud_block_photo_stream_sync(self) -> Optional[bool]:
        """Gets the iCloudBlockPhotoStreamSync property"""
        return self.properties.get("iCloudBlockPhotoStreamSync", None)

    @odata(name="iCloudBlockSharedPhotoStream")
    @property
    def icloud_block_shared_photo_stream(self) -> Optional[bool]:
        """Gets the iCloudBlockSharedPhotoStream property"""
        return self.properties.get("iCloudBlockSharedPhotoStream", None)

    @odata(name="iCloudRequireEncryptedBackup")
    @property
    def icloud_require_encrypted_backup(self) -> Optional[bool]:
        """Gets the iCloudRequireEncryptedBackup property"""
        return self.properties.get("iCloudRequireEncryptedBackup", None)

    @odata(name="iTunesBlockExplicitContent")
    @property
    def itunes_block_explicit_content(self) -> Optional[bool]:
        """Gets the iTunesBlockExplicitContent property"""
        return self.properties.get("iTunesBlockExplicitContent", None)

    @odata(name="iTunesBlockMusicService")
    @property
    def itunes_block_music_service(self) -> Optional[bool]:
        """Gets the iTunesBlockMusicService property"""
        return self.properties.get("iTunesBlockMusicService", None)

    @odata(name="iTunesBlockRadio")
    @property
    def itunes_block_radio(self) -> Optional[bool]:
        """Gets the iTunesBlockRadio property"""
        return self.properties.get("iTunesBlockRadio", None)

    @odata(name="keyboardBlockAutoCorrect")
    @property
    def keyboard_block_auto_correct(self) -> Optional[bool]:
        """Gets the keyboardBlockAutoCorrect property"""
        return self.properties.get("keyboardBlockAutoCorrect", None)

    @odata(name="keyboardBlockDictation")
    @property
    def keyboard_block_dictation(self) -> Optional[bool]:
        """Gets the keyboardBlockDictation property"""
        return self.properties.get("keyboardBlockDictation", None)

    @odata(name="keyboardBlockPredictive")
    @property
    def keyboard_block_predictive(self) -> Optional[bool]:
        """Gets the keyboardBlockPredictive property"""
        return self.properties.get("keyboardBlockPredictive", None)

    @odata(name="keyboardBlockShortcuts")
    @property
    def keyboard_block_shortcuts(self) -> Optional[bool]:
        """Gets the keyboardBlockShortcuts property"""
        return self.properties.get("keyboardBlockShortcuts", None)

    @odata(name="keyboardBlockSpellCheck")
    @property
    def keyboard_block_spell_check(self) -> Optional[bool]:
        """Gets the keyboardBlockSpellCheck property"""
        return self.properties.get("keyboardBlockSpellCheck", None)

    @odata(name="kioskModeAllowAssistiveSpeak")
    @property
    def kiosk_mode_allow_assistive_speak(self) -> Optional[bool]:
        """Gets the kioskModeAllowAssistiveSpeak property"""
        return self.properties.get("kioskModeAllowAssistiveSpeak", None)

    @odata(name="kioskModeAllowAssistiveTouchSettings")
    @property
    def kiosk_mode_allow_assistive_touch_settings(self) -> Optional[bool]:
        """Gets the kioskModeAllowAssistiveTouchSettings property"""
        return self.properties.get("kioskModeAllowAssistiveTouchSettings", None)

    @odata(name="kioskModeAllowAutoLock")
    @property
    def kiosk_mode_allow_auto_lock(self) -> Optional[bool]:
        """Gets the kioskModeAllowAutoLock property"""
        return self.properties.get("kioskModeAllowAutoLock", None)

    @odata(name="kioskModeAllowColorInversionSettings")
    @property
    def kiosk_mode_allow_color_inversion_settings(self) -> Optional[bool]:
        """Gets the kioskModeAllowColorInversionSettings property"""
        return self.properties.get("kioskModeAllowColorInversionSettings", None)

    @odata(name="kioskModeAllowRingerSwitch")
    @property
    def kiosk_mode_allow_ringer_switch(self) -> Optional[bool]:
        """Gets the kioskModeAllowRingerSwitch property"""
        return self.properties.get("kioskModeAllowRingerSwitch", None)

    @odata(name="kioskModeAllowScreenRotation")
    @property
    def kiosk_mode_allow_screen_rotation(self) -> Optional[bool]:
        """Gets the kioskModeAllowScreenRotation property"""
        return self.properties.get("kioskModeAllowScreenRotation", None)

    @odata(name="kioskModeAllowSleepButton")
    @property
    def kiosk_mode_allow_sleep_button(self) -> Optional[bool]:
        """Gets the kioskModeAllowSleepButton property"""
        return self.properties.get("kioskModeAllowSleepButton", None)

    @odata(name="kioskModeAllowTouchscreen")
    @property
    def kiosk_mode_allow_touchscreen(self) -> Optional[bool]:
        """Gets the kioskModeAllowTouchscreen property"""
        return self.properties.get("kioskModeAllowTouchscreen", None)

    @odata(name="kioskModeAllowVoiceOverSettings")
    @property
    def kiosk_mode_allow_voice_over_settings(self) -> Optional[bool]:
        """Gets the kioskModeAllowVoiceOverSettings property"""
        return self.properties.get("kioskModeAllowVoiceOverSettings", None)

    @odata(name="kioskModeAllowVolumeButtons")
    @property
    def kiosk_mode_allow_volume_buttons(self) -> Optional[bool]:
        """Gets the kioskModeAllowVolumeButtons property"""
        return self.properties.get("kioskModeAllowVolumeButtons", None)

    @odata(name="kioskModeAllowZoomSettings")
    @property
    def kiosk_mode_allow_zoom_settings(self) -> Optional[bool]:
        """Gets the kioskModeAllowZoomSettings property"""
        return self.properties.get("kioskModeAllowZoomSettings", None)

    @odata(name="kioskModeAppStoreUrl")
    @property
    def kiosk_mode_app_store_url(self) -> Optional[str]:
        """Gets the kioskModeAppStoreUrl property"""
        return self.properties.get("kioskModeAppStoreUrl", None)

    @odata(name="kioskModeBuiltInAppId")
    @property
    def kiosk_mode_built_in_app_id(self) -> Optional[str]:
        """Gets the kioskModeBuiltInAppId property"""
        return self.properties.get("kioskModeBuiltInAppId", None)

    @odata(name="kioskModeManagedAppId")
    @property
    def kiosk_mode_managed_app_id(self) -> Optional[str]:
        """Gets the kioskModeManagedAppId property"""
        return self.properties.get("kioskModeManagedAppId", None)

    @odata(name="kioskModeRequireAssistiveTouch")
    @property
    def kiosk_mode_require_assistive_touch(self) -> Optional[bool]:
        """Gets the kioskModeRequireAssistiveTouch property"""
        return self.properties.get("kioskModeRequireAssistiveTouch", None)

    @odata(name="kioskModeRequireColorInversion")
    @property
    def kiosk_mode_require_color_inversion(self) -> Optional[bool]:
        """Gets the kioskModeRequireColorInversion property"""
        return self.properties.get("kioskModeRequireColorInversion", None)

    @odata(name="kioskModeRequireMonoAudio")
    @property
    def kiosk_mode_require_mono_audio(self) -> Optional[bool]:
        """Gets the kioskModeRequireMonoAudio property"""
        return self.properties.get("kioskModeRequireMonoAudio", None)

    @odata(name="kioskModeRequireVoiceOver")
    @property
    def kiosk_mode_require_voice_over(self) -> Optional[bool]:
        """Gets the kioskModeRequireVoiceOver property"""
        return self.properties.get("kioskModeRequireVoiceOver", None)

    @odata(name="kioskModeRequireZoom")
    @property
    def kiosk_mode_require_zoom(self) -> Optional[bool]:
        """Gets the kioskModeRequireZoom property"""
        return self.properties.get("kioskModeRequireZoom", None)

    @odata(name="lockScreenBlockControlCenter")
    @property
    def lock_screen_block_control_center(self) -> Optional[bool]:
        """Gets the lockScreenBlockControlCenter property"""
        return self.properties.get("lockScreenBlockControlCenter", None)

    @odata(name="lockScreenBlockNotificationView")
    @property
    def lock_screen_block_notification_view(self) -> Optional[bool]:
        """Gets the lockScreenBlockNotificationView property"""
        return self.properties.get("lockScreenBlockNotificationView", None)

    @odata(name="lockScreenBlockPassbook")
    @property
    def lock_screen_block_passbook(self) -> Optional[bool]:
        """Gets the lockScreenBlockPassbook property"""
        return self.properties.get("lockScreenBlockPassbook", None)

    @odata(name="lockScreenBlockTodayView")
    @property
    def lock_screen_block_today_view(self) -> Optional[bool]:
        """Gets the lockScreenBlockTodayView property"""
        return self.properties.get("lockScreenBlockTodayView", None)

    @odata(name="mediaContentRatingApps")
    @property
    def media_content_rating_apps(self) -> RatingAppsType:
        """Gets the mediaContentRatingApps property"""
        return self.properties.get("mediaContentRatingApps", RatingAppsType.allAllowed)

    @odata(name="mediaContentRatingAustralia")
    @property
    def media_content_rating_australia(self) -> MediaContentRatingAustralia:
        """Gets the mediaContentRatingAustralia property"""
        return self.properties.get("mediaContentRatingAustralia", MediaContentRatingAustralia())

    @odata(name="mediaContentRatingCanada")
    @property
    def media_content_rating_canada(self) -> MediaContentRatingCanada:
        """Gets the mediaContentRatingCanada property"""
        return self.properties.get("mediaContentRatingCanada", MediaContentRatingCanada())

    @odata(name="mediaContentRatingFrance")
    @property
    def media_content_rating_france(self) -> MediaContentRatingFrance:
        """Gets the mediaContentRatingFrance property"""
        return self.properties.get("mediaContentRatingFrance", MediaContentRatingFrance())

    @odata(name="mediaContentRatingGermany")
    @property
    def media_content_rating_germany(self) -> MediaContentRatingGermany:
        """Gets the mediaContentRatingGermany property"""
        return self.properties.get("mediaContentRatingGermany", MediaContentRatingGermany())

    @odata(name="mediaContentRatingIreland")
    @property
    def media_content_rating_ireland(self) -> MediaContentRatingIreland:
        """Gets the mediaContentRatingIreland property"""
        return self.properties.get("mediaContentRatingIreland", MediaContentRatingIreland())

    @odata(name="mediaContentRatingJapan")
    @property
    def media_content_rating_japan(self) -> MediaContentRatingJapan:
        """Gets the mediaContentRatingJapan property"""
        return self.properties.get("mediaContentRatingJapan", MediaContentRatingJapan())

    @odata(name="mediaContentRatingNewZealand")
    @property
    def media_content_rating_new_zealand(self) -> MediaContentRatingNewZealand:
        """Gets the mediaContentRatingNewZealand property"""
        return self.properties.get("mediaContentRatingNewZealand", MediaContentRatingNewZealand())

    @odata(name="mediaContentRatingUnitedKingdom")
    @property
    def media_content_rating_united_kingdom(self) -> MediaContentRatingUnitedKingdom:
        """Gets the mediaContentRatingUnitedKingdom property"""
        return self.properties.get("mediaContentRatingUnitedKingdom", MediaContentRatingUnitedKingdom())

    @odata(name="mediaContentRatingUnitedStates")
    @property
    def media_content_rating_united_states(self) -> MediaContentRatingUnitedStates:
        """Gets the mediaContentRatingUnitedStates property"""
        return self.properties.get("mediaContentRatingUnitedStates", MediaContentRatingUnitedStates())

    @odata(name="messagesBlocked")
    @property
    def messages_blocked(self) -> Optional[bool]:
        """Gets the messagesBlocked property"""
        return self.properties.get("messagesBlocked", None)

    @odata(name="networkUsageRules")
    @property
    def network_usage_rules(self) -> ClientValueCollection[IosNetworkUsageRule]:
        """Gets the networkUsageRules property"""
        return self.properties.get("networkUsageRules", ClientValueCollection[IosNetworkUsageRule](IosNetworkUsageRule))

    @odata(name="notificationsBlockSettingsModification")
    @property
    def notifications_block_settings_modification(self) -> Optional[bool]:
        """Gets the notificationsBlockSettingsModification property"""
        return self.properties.get("notificationsBlockSettingsModification", None)

    @odata(name="passcodeBlockFingerprintModification")
    @property
    def passcode_block_fingerprint_modification(self) -> Optional[bool]:
        """Gets the passcodeBlockFingerprintModification property"""
        return self.properties.get("passcodeBlockFingerprintModification", None)

    @odata(name="passcodeBlockFingerprintUnlock")
    @property
    def passcode_block_fingerprint_unlock(self) -> Optional[bool]:
        """Gets the passcodeBlockFingerprintUnlock property"""
        return self.properties.get("passcodeBlockFingerprintUnlock", None)

    @odata(name="passcodeBlockModification")
    @property
    def passcode_block_modification(self) -> Optional[bool]:
        """Gets the passcodeBlockModification property"""
        return self.properties.get("passcodeBlockModification", None)

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

    @odata(name="passcodeMinutesOfInactivityBeforeScreenTimeout")
    @property
    def passcode_minutes_of_inactivity_before_screen_timeout(self) -> Optional[int]:
        """Gets the passcodeMinutesOfInactivityBeforeScreenTimeout property"""
        return self.properties.get("passcodeMinutesOfInactivityBeforeScreenTimeout", None)

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

    @odata(name="passcodeSignInFailureCountBeforeWipe")
    @property
    def passcode_sign_in_failure_count_before_wipe(self) -> Optional[int]:
        """Gets the passcodeSignInFailureCountBeforeWipe property"""
        return self.properties.get("passcodeSignInFailureCountBeforeWipe", None)

    @odata(name="podcastsBlocked")
    @property
    def podcasts_blocked(self) -> Optional[bool]:
        """Gets the podcastsBlocked property"""
        return self.properties.get("podcastsBlocked", None)

    @odata(name="safariBlockAutofill")
    @property
    def safari_block_autofill(self) -> Optional[bool]:
        """Gets the safariBlockAutofill property"""
        return self.properties.get("safariBlockAutofill", None)

    @odata(name="safariBlocked")
    @property
    def safari_blocked(self) -> Optional[bool]:
        """Gets the safariBlocked property"""
        return self.properties.get("safariBlocked", None)

    @odata(name="safariBlockJavaScript")
    @property
    def safari_block_java_script(self) -> Optional[bool]:
        """Gets the safariBlockJavaScript property"""
        return self.properties.get("safariBlockJavaScript", None)

    @odata(name="safariBlockPopups")
    @property
    def safari_block_popups(self) -> Optional[bool]:
        """Gets the safariBlockPopups property"""
        return self.properties.get("safariBlockPopups", None)

    @odata(name="safariCookieSettings")
    @property
    def safari_cookie_settings(self) -> WebBrowserCookieSettings:
        """Gets the safariCookieSettings property"""
        return self.properties.get("safariCookieSettings", WebBrowserCookieSettings.browserDefault)

    @odata(name="safariManagedDomains")
    @property
    def safari_managed_domains(self) -> StringCollection:
        """Gets the safariManagedDomains property"""
        return self.properties.get("safariManagedDomains", StringCollection())

    @odata(name="safariPasswordAutoFillDomains")
    @property
    def safari_password_auto_fill_domains(self) -> StringCollection:
        """Gets the safariPasswordAutoFillDomains property"""
        return self.properties.get("safariPasswordAutoFillDomains", StringCollection())

    @odata(name="safariRequireFraudWarning")
    @property
    def safari_require_fraud_warning(self) -> Optional[bool]:
        """Gets the safariRequireFraudWarning property"""
        return self.properties.get("safariRequireFraudWarning", None)

    @odata(name="screenCaptureBlocked")
    @property
    def screen_capture_blocked(self) -> Optional[bool]:
        """Gets the screenCaptureBlocked property"""
        return self.properties.get("screenCaptureBlocked", None)

    @odata(name="siriBlocked")
    @property
    def siri_blocked(self) -> Optional[bool]:
        """Gets the siriBlocked property"""
        return self.properties.get("siriBlocked", None)

    @odata(name="siriBlockedWhenLocked")
    @property
    def siri_blocked_when_locked(self) -> Optional[bool]:
        """Gets the siriBlockedWhenLocked property"""
        return self.properties.get("siriBlockedWhenLocked", None)

    @odata(name="siriBlockUserGeneratedContent")
    @property
    def siri_block_user_generated_content(self) -> Optional[bool]:
        """Gets the siriBlockUserGeneratedContent property"""
        return self.properties.get("siriBlockUserGeneratedContent", None)

    @odata(name="siriRequireProfanityFilter")
    @property
    def siri_require_profanity_filter(self) -> Optional[bool]:
        """Gets the siriRequireProfanityFilter property"""
        return self.properties.get("siriRequireProfanityFilter", None)

    @odata(name="spotlightBlockInternetResults")
    @property
    def spotlight_block_internet_results(self) -> Optional[bool]:
        """Gets the spotlightBlockInternetResults property"""
        return self.properties.get("spotlightBlockInternetResults", None)

    @odata(name="voiceDialingBlocked")
    @property
    def voice_dialing_blocked(self) -> Optional[bool]:
        """Gets the voiceDialingBlocked property"""
        return self.properties.get("voiceDialingBlocked", None)

    @odata(name="wallpaperBlockModification")
    @property
    def wallpaper_block_modification(self) -> Optional[bool]:
        """Gets the wallpaperBlockModification property"""
        return self.properties.get("wallpaperBlockModification", None)

    @odata(name="wiFiConnectOnlyToConfiguredNetworks")
    @property
    def wi_fi_connect_only_to_configured_networks(self) -> Optional[bool]:
        """Gets the wiFiConnectOnlyToConfiguredNetworks property"""
        return self.properties.get("wiFiConnectOnlyToConfiguredNetworks", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosGeneralDeviceConfiguration"
