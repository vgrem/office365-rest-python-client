from __future__ import annotations

from datetime import time
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.requiredpasswordtype import RequiredPasswordType
from office365.intune.devices.configurations.edge_search_engine_base import EdgeSearchEngineBase
from office365.intune.devices.configurations.windows.general.defendercloudblockleveltype import (  # noqa: E501
    DefenderCloudBlockLevelType,
)
from office365.intune.devices.configurations.windows.general.defendermonitorfileactivity import (  # noqa: E501
    DefenderMonitorFileActivity,
)
from office365.intune.devices.configurations.windows.general.defenderpromptforsamplesubmission import (  # noqa: E501
    DefenderPromptForSampleSubmission,
)
from office365.intune.devices.configurations.windows.general.defenderscantype import DefenderScanType
from office365.intune.devices.configurations.windows.general.diagnosticdatasubmissionmode import (  # noqa: E501
    DiagnosticDataSubmissionMode,
)
from office365.intune.devices.configurations.windows.general.edgecookiepolicy import EdgeCookiePolicy
from office365.intune.devices.configurations.windows.safesearchfiltertype import SafeSearchFilterType
from office365.intune.devices.configurations.windows.spotlightenablementsettings import (  # noqa: E501
    WindowsSpotlightEnablementSettings,
)
from office365.intune.devices.configurations.windows.startmenuapplistvisibilitytype import (  # noqa: E501
    WindowsStartMenuAppListVisibilityType,
)
from office365.intune.devices.configurations.windows.startmenumodetype import WindowsStartMenuModeType
from office365.intune.devices.configurations.windows.statemanagementsetting import StateManagementSetting
from office365.intune.devices.configurations.windows.visibilitysetting import VisibilitySetting
from office365.intune.devices.configurations.windows.weeklyschedule import WeeklySchedule
from office365.intune.devices.configurations.windows.windows10_network_proxy_server import Windows10NetworkProxyServer
from office365.intune.devices.management.defender_detected_malware_actions import DefenderDetectedMalwareActions
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class Windows10GeneralConfiguration(Entity):
    @odata(name="accountsBlockAddingNonMicrosoftAccountEmail")
    @property
    def accounts_block_adding_non_microsoft_account_email(self) -> Optional[bool]:
        """Gets the accountsBlockAddingNonMicrosoftAccountEmail property"""
        return self.properties.get("accountsBlockAddingNonMicrosoftAccountEmail", None)

    @odata(name="antiTheftModeBlocked")
    @property
    def anti_theft_mode_blocked(self) -> Optional[bool]:
        """Gets the antiTheftModeBlocked property"""
        return self.properties.get("antiTheftModeBlocked", None)

    @odata(name="appsAllowTrustedAppsSideloading")
    @property
    def apps_allow_trusted_apps_sideloading(self) -> StateManagementSetting:
        """Gets the appsAllowTrustedAppsSideloading property"""
        return self.properties.get("appsAllowTrustedAppsSideloading", StateManagementSetting.notConfigured)

    @odata(name="appsBlockWindowsStoreOriginatedApps")
    @property
    def apps_block_windows_store_originated_apps(self) -> Optional[bool]:
        """Gets the appsBlockWindowsStoreOriginatedApps property"""
        return self.properties.get("appsBlockWindowsStoreOriginatedApps", None)

    @odata(name="bluetoothAllowedServices")
    @property
    def bluetooth_allowed_services(self) -> StringCollection:
        """Gets the bluetoothAllowedServices property"""
        return self.properties.get("bluetoothAllowedServices", StringCollection())

    @odata(name="bluetoothBlockAdvertising")
    @property
    def bluetooth_block_advertising(self) -> Optional[bool]:
        """Gets the bluetoothBlockAdvertising property"""
        return self.properties.get("bluetoothBlockAdvertising", None)

    @odata(name="bluetoothBlockDiscoverableMode")
    @property
    def bluetooth_block_discoverable_mode(self) -> Optional[bool]:
        """Gets the bluetoothBlockDiscoverableMode property"""
        return self.properties.get("bluetoothBlockDiscoverableMode", None)

    @odata(name="bluetoothBlocked")
    @property
    def bluetooth_blocked(self) -> Optional[bool]:
        """Gets the bluetoothBlocked property"""
        return self.properties.get("bluetoothBlocked", None)

    @odata(name="bluetoothBlockPrePairing")
    @property
    def bluetooth_block_pre_pairing(self) -> Optional[bool]:
        """Gets the bluetoothBlockPrePairing property"""
        return self.properties.get("bluetoothBlockPrePairing", None)

    @odata(name="cameraBlocked")
    @property
    def camera_blocked(self) -> Optional[bool]:
        """Gets the cameraBlocked property"""
        return self.properties.get("cameraBlocked", None)

    @odata(name="cellularBlockDataWhenRoaming")
    @property
    def cellular_block_data_when_roaming(self) -> Optional[bool]:
        """Gets the cellularBlockDataWhenRoaming property"""
        return self.properties.get("cellularBlockDataWhenRoaming", None)

    @odata(name="cellularBlockVpn")
    @property
    def cellular_block_vpn(self) -> Optional[bool]:
        """Gets the cellularBlockVpn property"""
        return self.properties.get("cellularBlockVpn", None)

    @odata(name="cellularBlockVpnWhenRoaming")
    @property
    def cellular_block_vpn_when_roaming(self) -> Optional[bool]:
        """Gets the cellularBlockVpnWhenRoaming property"""
        return self.properties.get("cellularBlockVpnWhenRoaming", None)

    @odata(name="certificatesBlockManualRootCertificateInstallation")
    @property
    def certificates_block_manual_root_certificate_installation(self) -> Optional[bool]:
        """Gets the certificatesBlockManualRootCertificateInstallation property"""
        return self.properties.get("certificatesBlockManualRootCertificateInstallation", None)

    @odata(name="connectedDevicesServiceBlocked")
    @property
    def connected_devices_service_blocked(self) -> Optional[bool]:
        """Gets the connectedDevicesServiceBlocked property"""
        return self.properties.get("connectedDevicesServiceBlocked", None)

    @odata(name="copyPasteBlocked")
    @property
    def copy_paste_blocked(self) -> Optional[bool]:
        """Gets the copyPasteBlocked property"""
        return self.properties.get("copyPasteBlocked", None)

    @odata(name="cortanaBlocked")
    @property
    def cortana_blocked(self) -> Optional[bool]:
        """Gets the cortanaBlocked property"""
        return self.properties.get("cortanaBlocked", None)

    @odata(name="defenderBlockEndUserAccess")
    @property
    def defender_block_end_user_access(self) -> Optional[bool]:
        """Gets the defenderBlockEndUserAccess property"""
        return self.properties.get("defenderBlockEndUserAccess", None)

    @odata(name="defenderCloudBlockLevel")
    @property
    def defender_cloud_block_level(self) -> DefenderCloudBlockLevelType:
        """Gets the defenderCloudBlockLevel property"""
        return self.properties.get("defenderCloudBlockLevel", DefenderCloudBlockLevelType.notConfigured)

    @odata(name="defenderDaysBeforeDeletingQuarantinedMalware")
    @property
    def defender_days_before_deleting_quarantined_malware(self) -> Optional[int]:
        """Gets the defenderDaysBeforeDeletingQuarantinedMalware property"""
        return self.properties.get("defenderDaysBeforeDeletingQuarantinedMalware", None)

    @odata(name="defenderDetectedMalwareActions")
    @property
    def defender_detected_malware_actions(self) -> DefenderDetectedMalwareActions:
        """Gets the defenderDetectedMalwareActions property"""
        return self.properties.get("defenderDetectedMalwareActions", DefenderDetectedMalwareActions())

    @odata(name="defenderFileExtensionsToExclude")
    @property
    def defender_file_extensions_to_exclude(self) -> StringCollection:
        """Gets the defenderFileExtensionsToExclude property"""
        return self.properties.get("defenderFileExtensionsToExclude", StringCollection())

    @odata(name="defenderFilesAndFoldersToExclude")
    @property
    def defender_files_and_folders_to_exclude(self) -> StringCollection:
        """Gets the defenderFilesAndFoldersToExclude property"""
        return self.properties.get("defenderFilesAndFoldersToExclude", StringCollection())

    @odata(name="defenderMonitorFileActivity")
    @property
    def defender_monitor_file_activity(self) -> DefenderMonitorFileActivity:
        """Gets the defenderMonitorFileActivity property"""
        return self.properties.get("defenderMonitorFileActivity", DefenderMonitorFileActivity.userDefined)

    @odata(name="defenderProcessesToExclude")
    @property
    def defender_processes_to_exclude(self) -> StringCollection:
        """Gets the defenderProcessesToExclude property"""
        return self.properties.get("defenderProcessesToExclude", StringCollection())

    @odata(name="defenderPromptForSampleSubmission")
    @property
    def defender_prompt_for_sample_submission(self) -> DefenderPromptForSampleSubmission:
        """Gets the defenderPromptForSampleSubmission property"""
        return self.properties.get("defenderPromptForSampleSubmission", DefenderPromptForSampleSubmission.userDefined)

    @odata(name="defenderRequireBehaviorMonitoring")
    @property
    def defender_require_behavior_monitoring(self) -> Optional[bool]:
        """Gets the defenderRequireBehaviorMonitoring property"""
        return self.properties.get("defenderRequireBehaviorMonitoring", None)

    @odata(name="defenderRequireCloudProtection")
    @property
    def defender_require_cloud_protection(self) -> Optional[bool]:
        """Gets the defenderRequireCloudProtection property"""
        return self.properties.get("defenderRequireCloudProtection", None)

    @odata(name="defenderRequireNetworkInspectionSystem")
    @property
    def defender_require_network_inspection_system(self) -> Optional[bool]:
        """Gets the defenderRequireNetworkInspectionSystem property"""
        return self.properties.get("defenderRequireNetworkInspectionSystem", None)

    @odata(name="defenderRequireRealTimeMonitoring")
    @property
    def defender_require_real_time_monitoring(self) -> Optional[bool]:
        """Gets the defenderRequireRealTimeMonitoring property"""
        return self.properties.get("defenderRequireRealTimeMonitoring", None)

    @odata(name="defenderScanArchiveFiles")
    @property
    def defender_scan_archive_files(self) -> Optional[bool]:
        """Gets the defenderScanArchiveFiles property"""
        return self.properties.get("defenderScanArchiveFiles", None)

    @odata(name="defenderScanDownloads")
    @property
    def defender_scan_downloads(self) -> Optional[bool]:
        """Gets the defenderScanDownloads property"""
        return self.properties.get("defenderScanDownloads", None)

    @odata(name="defenderScanIncomingMail")
    @property
    def defender_scan_incoming_mail(self) -> Optional[bool]:
        """Gets the defenderScanIncomingMail property"""
        return self.properties.get("defenderScanIncomingMail", None)

    @odata(name="defenderScanMappedNetworkDrivesDuringFullScan")
    @property
    def defender_scan_mapped_network_drives_during_full_scan(self) -> Optional[bool]:
        """Gets the defenderScanMappedNetworkDrivesDuringFullScan property"""
        return self.properties.get("defenderScanMappedNetworkDrivesDuringFullScan", None)

    @odata(name="defenderScanMaxCpu")
    @property
    def defender_scan_max_cpu(self) -> Optional[int]:
        """Gets the defenderScanMaxCpu property"""
        return self.properties.get("defenderScanMaxCpu", None)

    @odata(name="defenderScanNetworkFiles")
    @property
    def defender_scan_network_files(self) -> Optional[bool]:
        """Gets the defenderScanNetworkFiles property"""
        return self.properties.get("defenderScanNetworkFiles", None)

    @odata(name="defenderScanRemovableDrivesDuringFullScan")
    @property
    def defender_scan_removable_drives_during_full_scan(self) -> Optional[bool]:
        """Gets the defenderScanRemovableDrivesDuringFullScan property"""
        return self.properties.get("defenderScanRemovableDrivesDuringFullScan", None)

    @odata(name="defenderScanScriptsLoadedInInternetExplorer")
    @property
    def defender_scan_scripts_loaded_in_internet_explorer(self) -> Optional[bool]:
        """Gets the defenderScanScriptsLoadedInInternetExplorer property"""
        return self.properties.get("defenderScanScriptsLoadedInInternetExplorer", None)

    @odata(name="defenderScanType")
    @property
    def defender_scan_type(self) -> DefenderScanType:
        """Gets the defenderScanType property"""
        return self.properties.get("defenderScanType", DefenderScanType.userDefined)

    @odata(name="defenderScheduledQuickScanTime")
    @property
    def defender_scheduled_quick_scan_time(self) -> Optional[time]:
        """Gets the defenderScheduledQuickScanTime property"""
        return self.properties.get("defenderScheduledQuickScanTime", None)

    @odata(name="defenderScheduledScanTime")
    @property
    def defender_scheduled_scan_time(self) -> Optional[time]:
        """Gets the defenderScheduledScanTime property"""
        return self.properties.get("defenderScheduledScanTime", None)

    @odata(name="defenderSignatureUpdateIntervalInHours")
    @property
    def defender_signature_update_interval_in_hours(self) -> Optional[int]:
        """Gets the defenderSignatureUpdateIntervalInHours property"""
        return self.properties.get("defenderSignatureUpdateIntervalInHours", None)

    @odata(name="defenderSystemScanSchedule")
    @property
    def defender_system_scan_schedule(self) -> WeeklySchedule:
        """Gets the defenderSystemScanSchedule property"""
        return self.properties.get("defenderSystemScanSchedule", WeeklySchedule.userDefined)

    @odata(name="developerUnlockSetting")
    @property
    def developer_unlock_setting(self) -> StateManagementSetting:
        """Gets the developerUnlockSetting property"""
        return self.properties.get("developerUnlockSetting", StateManagementSetting.notConfigured)

    @odata(name="deviceManagementBlockFactoryResetOnMobile")
    @property
    def device_management_block_factory_reset_on_mobile(self) -> Optional[bool]:
        """Gets the deviceManagementBlockFactoryResetOnMobile property"""
        return self.properties.get("deviceManagementBlockFactoryResetOnMobile", None)

    @odata(name="deviceManagementBlockManualUnenroll")
    @property
    def device_management_block_manual_unenroll(self) -> Optional[bool]:
        """Gets the deviceManagementBlockManualUnenroll property"""
        return self.properties.get("deviceManagementBlockManualUnenroll", None)

    @odata(name="diagnosticsDataSubmissionMode")
    @property
    def diagnostics_data_submission_mode(self) -> DiagnosticDataSubmissionMode:
        """Gets the diagnosticsDataSubmissionMode property"""
        return self.properties.get("diagnosticsDataSubmissionMode", DiagnosticDataSubmissionMode.userDefined)

    @odata(name="edgeAllowStartPagesModification")
    @property
    def edge_allow_start_pages_modification(self) -> Optional[bool]:
        """Gets the edgeAllowStartPagesModification property"""
        return self.properties.get("edgeAllowStartPagesModification", None)

    @odata(name="edgeBlockAccessToAboutFlags")
    @property
    def edge_block_access_to_about_flags(self) -> Optional[bool]:
        """Gets the edgeBlockAccessToAboutFlags property"""
        return self.properties.get("edgeBlockAccessToAboutFlags", None)

    @odata(name="edgeBlockAddressBarDropdown")
    @property
    def edge_block_address_bar_dropdown(self) -> Optional[bool]:
        """Gets the edgeBlockAddressBarDropdown property"""
        return self.properties.get("edgeBlockAddressBarDropdown", None)

    @odata(name="edgeBlockAutofill")
    @property
    def edge_block_autofill(self) -> Optional[bool]:
        """Gets the edgeBlockAutofill property"""
        return self.properties.get("edgeBlockAutofill", None)

    @odata(name="edgeBlockCompatibilityList")
    @property
    def edge_block_compatibility_list(self) -> Optional[bool]:
        """Gets the edgeBlockCompatibilityList property"""
        return self.properties.get("edgeBlockCompatibilityList", None)

    @odata(name="edgeBlockDeveloperTools")
    @property
    def edge_block_developer_tools(self) -> Optional[bool]:
        """Gets the edgeBlockDeveloperTools property"""
        return self.properties.get("edgeBlockDeveloperTools", None)

    @odata(name="edgeBlocked")
    @property
    def edge_blocked(self) -> Optional[bool]:
        """Gets the edgeBlocked property"""
        return self.properties.get("edgeBlocked", None)

    @odata(name="edgeBlockExtensions")
    @property
    def edge_block_extensions(self) -> Optional[bool]:
        """Gets the edgeBlockExtensions property"""
        return self.properties.get("edgeBlockExtensions", None)

    @odata(name="edgeBlockInPrivateBrowsing")
    @property
    def edge_block_in_private_browsing(self) -> Optional[bool]:
        """Gets the edgeBlockInPrivateBrowsing property"""
        return self.properties.get("edgeBlockInPrivateBrowsing", None)

    @odata(name="edgeBlockJavaScript")
    @property
    def edge_block_java_script(self) -> Optional[bool]:
        """Gets the edgeBlockJavaScript property"""
        return self.properties.get("edgeBlockJavaScript", None)

    @odata(name="edgeBlockLiveTileDataCollection")
    @property
    def edge_block_live_tile_data_collection(self) -> Optional[bool]:
        """Gets the edgeBlockLiveTileDataCollection property"""
        return self.properties.get("edgeBlockLiveTileDataCollection", None)

    @odata(name="edgeBlockPasswordManager")
    @property
    def edge_block_password_manager(self) -> Optional[bool]:
        """Gets the edgeBlockPasswordManager property"""
        return self.properties.get("edgeBlockPasswordManager", None)

    @odata(name="edgeBlockPopups")
    @property
    def edge_block_popups(self) -> Optional[bool]:
        """Gets the edgeBlockPopups property"""
        return self.properties.get("edgeBlockPopups", None)

    @odata(name="edgeBlockSearchSuggestions")
    @property
    def edge_block_search_suggestions(self) -> Optional[bool]:
        """Gets the edgeBlockSearchSuggestions property"""
        return self.properties.get("edgeBlockSearchSuggestions", None)

    @odata(name="edgeBlockSendingDoNotTrackHeader")
    @property
    def edge_block_sending_do_not_track_header(self) -> Optional[bool]:
        """Gets the edgeBlockSendingDoNotTrackHeader property"""
        return self.properties.get("edgeBlockSendingDoNotTrackHeader", None)

    @odata(name="edgeBlockSendingIntranetTrafficToInternetExplorer")
    @property
    def edge_block_sending_intranet_traffic_to_internet_explorer(self) -> Optional[bool]:
        """Gets the edgeBlockSendingIntranetTrafficToInternetExplorer property"""
        return self.properties.get("edgeBlockSendingIntranetTrafficToInternetExplorer", None)

    @odata(name="edgeClearBrowsingDataOnExit")
    @property
    def edge_clear_browsing_data_on_exit(self) -> Optional[bool]:
        """Gets the edgeClearBrowsingDataOnExit property"""
        return self.properties.get("edgeClearBrowsingDataOnExit", None)

    @odata(name="edgeCookiePolicy")
    @property
    def edge_cookie_policy(self) -> EdgeCookiePolicy:
        """Gets the edgeCookiePolicy property"""
        return self.properties.get("edgeCookiePolicy", EdgeCookiePolicy.userDefined)

    @odata(name="edgeDisableFirstRunPage")
    @property
    def edge_disable_first_run_page(self) -> Optional[bool]:
        """Gets the edgeDisableFirstRunPage property"""
        return self.properties.get("edgeDisableFirstRunPage", None)

    @odata(name="edgeEnterpriseModeSiteListLocation")
    @property
    def edge_enterprise_mode_site_list_location(self) -> Optional[str]:
        """Gets the edgeEnterpriseModeSiteListLocation property"""
        return self.properties.get("edgeEnterpriseModeSiteListLocation", None)

    @odata(name="edgeFirstRunUrl")
    @property
    def edge_first_run_url(self) -> Optional[str]:
        """Gets the edgeFirstRunUrl property"""
        return self.properties.get("edgeFirstRunUrl", None)

    @odata(name="edgeHomepageUrls")
    @property
    def edge_homepage_urls(self) -> StringCollection:
        """Gets the edgeHomepageUrls property"""
        return self.properties.get("edgeHomepageUrls", StringCollection())

    @odata(name="edgeRequireSmartScreen")
    @property
    def edge_require_smart_screen(self) -> Optional[bool]:
        """Gets the edgeRequireSmartScreen property"""
        return self.properties.get("edgeRequireSmartScreen", None)

    @odata(name="edgeSearchEngine")
    @property
    def edge_search_engine(self) -> EdgeSearchEngineBase:
        """Gets the edgeSearchEngine property"""
        return self.properties.get("edgeSearchEngine", EdgeSearchEngineBase())

    @odata(name="edgeSendIntranetTrafficToInternetExplorer")
    @property
    def edge_send_intranet_traffic_to_internet_explorer(self) -> Optional[bool]:
        """Gets the edgeSendIntranetTrafficToInternetExplorer property"""
        return self.properties.get("edgeSendIntranetTrafficToInternetExplorer", None)

    @odata(name="edgeSyncFavoritesWithInternetExplorer")
    @property
    def edge_sync_favorites_with_internet_explorer(self) -> Optional[bool]:
        """Gets the edgeSyncFavoritesWithInternetExplorer property"""
        return self.properties.get("edgeSyncFavoritesWithInternetExplorer", None)

    @odata(name="enterpriseCloudPrintDiscoveryEndPoint")
    @property
    def enterprise_cloud_print_discovery_end_point(self) -> Optional[str]:
        """Gets the enterpriseCloudPrintDiscoveryEndPoint property"""
        return self.properties.get("enterpriseCloudPrintDiscoveryEndPoint", None)

    @odata(name="enterpriseCloudPrintDiscoveryMaxLimit")
    @property
    def enterprise_cloud_print_discovery_max_limit(self) -> Optional[int]:
        """Gets the enterpriseCloudPrintDiscoveryMaxLimit property"""
        return self.properties.get("enterpriseCloudPrintDiscoveryMaxLimit", None)

    @odata(name="enterpriseCloudPrintMopriaDiscoveryResourceIdentifier")
    @property
    def enterprise_cloud_print_mopria_discovery_resource_identifier(self) -> Optional[str]:
        """Gets the enterpriseCloudPrintMopriaDiscoveryResourceIdentifier property"""
        return self.properties.get("enterpriseCloudPrintMopriaDiscoveryResourceIdentifier", None)

    @odata(name="enterpriseCloudPrintOAuthAuthority")
    @property
    def enterprise_cloud_print_o_auth_authority(self) -> Optional[str]:
        """Gets the enterpriseCloudPrintOAuthAuthority property"""
        return self.properties.get("enterpriseCloudPrintOAuthAuthority", None)

    @odata(name="enterpriseCloudPrintOAuthClientIdentifier")
    @property
    def enterprise_cloud_print_o_auth_client_identifier(self) -> Optional[str]:
        """Gets the enterpriseCloudPrintOAuthClientIdentifier property"""
        return self.properties.get("enterpriseCloudPrintOAuthClientIdentifier", None)

    @odata(name="enterpriseCloudPrintResourceIdentifier")
    @property
    def enterprise_cloud_print_resource_identifier(self) -> Optional[str]:
        """Gets the enterpriseCloudPrintResourceIdentifier property"""
        return self.properties.get("enterpriseCloudPrintResourceIdentifier", None)

    @odata(name="experienceBlockDeviceDiscovery")
    @property
    def experience_block_device_discovery(self) -> Optional[bool]:
        """Gets the experienceBlockDeviceDiscovery property"""
        return self.properties.get("experienceBlockDeviceDiscovery", None)

    @odata(name="experienceBlockErrorDialogWhenNoSIM")
    @property
    def experience_block_error_dialog_when_no_sim(self) -> Optional[bool]:
        """Gets the experienceBlockErrorDialogWhenNoSIM property"""
        return self.properties.get("experienceBlockErrorDialogWhenNoSIM", None)

    @odata(name="experienceBlockTaskSwitcher")
    @property
    def experience_block_task_switcher(self) -> Optional[bool]:
        """Gets the experienceBlockTaskSwitcher property"""
        return self.properties.get("experienceBlockTaskSwitcher", None)

    @odata(name="gameDvrBlocked")
    @property
    def game_dvr_blocked(self) -> Optional[bool]:
        """Gets the gameDvrBlocked property"""
        return self.properties.get("gameDvrBlocked", None)

    @odata(name="internetSharingBlocked")
    @property
    def internet_sharing_blocked(self) -> Optional[bool]:
        """Gets the internetSharingBlocked property"""
        return self.properties.get("internetSharingBlocked", None)

    @odata(name="locationServicesBlocked")
    @property
    def location_services_blocked(self) -> Optional[bool]:
        """Gets the locationServicesBlocked property"""
        return self.properties.get("locationServicesBlocked", None)

    @odata(name="lockScreenAllowTimeoutConfiguration")
    @property
    def lock_screen_allow_timeout_configuration(self) -> Optional[bool]:
        """Gets the lockScreenAllowTimeoutConfiguration property"""
        return self.properties.get("lockScreenAllowTimeoutConfiguration", None)

    @odata(name="lockScreenBlockActionCenterNotifications")
    @property
    def lock_screen_block_action_center_notifications(self) -> Optional[bool]:
        """Gets the lockScreenBlockActionCenterNotifications property"""
        return self.properties.get("lockScreenBlockActionCenterNotifications", None)

    @odata(name="lockScreenBlockCortana")
    @property
    def lock_screen_block_cortana(self) -> Optional[bool]:
        """Gets the lockScreenBlockCortana property"""
        return self.properties.get("lockScreenBlockCortana", None)

    @odata(name="lockScreenBlockToastNotifications")
    @property
    def lock_screen_block_toast_notifications(self) -> Optional[bool]:
        """Gets the lockScreenBlockToastNotifications property"""
        return self.properties.get("lockScreenBlockToastNotifications", None)

    @odata(name="lockScreenTimeoutInSeconds")
    @property
    def lock_screen_timeout_in_seconds(self) -> Optional[int]:
        """Gets the lockScreenTimeoutInSeconds property"""
        return self.properties.get("lockScreenTimeoutInSeconds", None)

    @odata(name="logonBlockFastUserSwitching")
    @property
    def logon_block_fast_user_switching(self) -> Optional[bool]:
        """Gets the logonBlockFastUserSwitching property"""
        return self.properties.get("logonBlockFastUserSwitching", None)

    @odata(name="microsoftAccountBlocked")
    @property
    def microsoft_account_blocked(self) -> Optional[bool]:
        """Gets the microsoftAccountBlocked property"""
        return self.properties.get("microsoftAccountBlocked", None)

    @odata(name="microsoftAccountBlockSettingsSync")
    @property
    def microsoft_account_block_settings_sync(self) -> Optional[bool]:
        """Gets the microsoftAccountBlockSettingsSync property"""
        return self.properties.get("microsoftAccountBlockSettingsSync", None)

    @odata(name="networkProxyApplySettingsDeviceWide")
    @property
    def network_proxy_apply_settings_device_wide(self) -> Optional[bool]:
        """Gets the networkProxyApplySettingsDeviceWide property"""
        return self.properties.get("networkProxyApplySettingsDeviceWide", None)

    @odata(name="networkProxyAutomaticConfigurationUrl")
    @property
    def network_proxy_automatic_configuration_url(self) -> Optional[str]:
        """Gets the networkProxyAutomaticConfigurationUrl property"""
        return self.properties.get("networkProxyAutomaticConfigurationUrl", None)

    @odata(name="networkProxyDisableAutoDetect")
    @property
    def network_proxy_disable_auto_detect(self) -> Optional[bool]:
        """Gets the networkProxyDisableAutoDetect property"""
        return self.properties.get("networkProxyDisableAutoDetect", None)

    @odata(name="networkProxyServer")
    @property
    def network_proxy_server(self) -> Optional[Windows10NetworkProxyServer]:
        """Gets the networkProxyServer property"""
        return self.properties.get("networkProxyServer", None)

    @odata(name="nfcBlocked")
    @property
    def nfc_blocked(self) -> Optional[bool]:
        """Gets the nfcBlocked property"""
        return self.properties.get("nfcBlocked", None)

    @odata(name="oneDriveDisableFileSync")
    @property
    def onedrive_disable_file_sync(self) -> Optional[bool]:
        """Gets the oneDriveDisableFileSync property"""
        return self.properties.get("oneDriveDisableFileSync", None)

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
    def password_required_type(self) -> RequiredPasswordType:
        """Gets the passwordRequiredType property"""
        return self.properties.get("passwordRequiredType", RequiredPasswordType.deviceDefault)

    @odata(name="passwordRequireWhenResumeFromIdleState")
    @property
    def password_require_when_resume_from_idle_state(self) -> Optional[bool]:
        """Gets the passwordRequireWhenResumeFromIdleState property"""
        return self.properties.get("passwordRequireWhenResumeFromIdleState", None)

    @odata(name="passwordSignInFailureCountBeforeFactoryReset")
    @property
    def password_sign_in_failure_count_before_factory_reset(self) -> Optional[int]:
        """Gets the passwordSignInFailureCountBeforeFactoryReset property"""
        return self.properties.get("passwordSignInFailureCountBeforeFactoryReset", None)

    @odata(name="personalizationDesktopImageUrl")
    @property
    def personalization_desktop_image_url(self) -> Optional[str]:
        """Gets the personalizationDesktopImageUrl property"""
        return self.properties.get("personalizationDesktopImageUrl", None)

    @odata(name="personalizationLockScreenImageUrl")
    @property
    def personalization_lock_screen_image_url(self) -> Optional[str]:
        """Gets the personalizationLockScreenImageUrl property"""
        return self.properties.get("personalizationLockScreenImageUrl", None)

    @odata(name="privacyAdvertisingId")
    @property
    def privacy_advertising_id(self) -> StateManagementSetting:
        """Gets the privacyAdvertisingId property"""
        return self.properties.get("privacyAdvertisingId", StateManagementSetting.notConfigured)

    @odata(name="privacyAutoAcceptPairingAndConsentPrompts")
    @property
    def privacy_auto_accept_pairing_and_consent_prompts(self) -> Optional[bool]:
        """Gets the privacyAutoAcceptPairingAndConsentPrompts property"""
        return self.properties.get("privacyAutoAcceptPairingAndConsentPrompts", None)

    @odata(name="privacyBlockInputPersonalization")
    @property
    def privacy_block_input_personalization(self) -> Optional[bool]:
        """Gets the privacyBlockInputPersonalization property"""
        return self.properties.get("privacyBlockInputPersonalization", None)

    @odata(name="resetProtectionModeBlocked")
    @property
    def reset_protection_mode_blocked(self) -> Optional[bool]:
        """Gets the resetProtectionModeBlocked property"""
        return self.properties.get("resetProtectionModeBlocked", None)

    @odata(name="safeSearchFilter")
    @property
    def safe_search_filter(self) -> SafeSearchFilterType:
        """Gets the safeSearchFilter property"""
        return self.properties.get("safeSearchFilter", SafeSearchFilterType.userDefined)

    @odata(name="screenCaptureBlocked")
    @property
    def screen_capture_blocked(self) -> Optional[bool]:
        """Gets the screenCaptureBlocked property"""
        return self.properties.get("screenCaptureBlocked", None)

    @odata(name="searchBlockDiacritics")
    @property
    def search_block_diacritics(self) -> Optional[bool]:
        """Gets the searchBlockDiacritics property"""
        return self.properties.get("searchBlockDiacritics", None)

    @odata(name="searchDisableAutoLanguageDetection")
    @property
    def search_disable_auto_language_detection(self) -> Optional[bool]:
        """Gets the searchDisableAutoLanguageDetection property"""
        return self.properties.get("searchDisableAutoLanguageDetection", None)

    @odata(name="searchDisableIndexerBackoff")
    @property
    def search_disable_indexer_backoff(self) -> Optional[bool]:
        """Gets the searchDisableIndexerBackoff property"""
        return self.properties.get("searchDisableIndexerBackoff", None)

    @odata(name="searchDisableIndexingEncryptedItems")
    @property
    def search_disable_indexing_encrypted_items(self) -> Optional[bool]:
        """Gets the searchDisableIndexingEncryptedItems property"""
        return self.properties.get("searchDisableIndexingEncryptedItems", None)

    @odata(name="searchDisableIndexingRemovableDrive")
    @property
    def search_disable_indexing_removable_drive(self) -> Optional[bool]:
        """Gets the searchDisableIndexingRemovableDrive property"""
        return self.properties.get("searchDisableIndexingRemovableDrive", None)

    @odata(name="searchEnableAutomaticIndexSizeManangement")
    @property
    def search_enable_automatic_index_size_manangement(self) -> Optional[bool]:
        """Gets the searchEnableAutomaticIndexSizeManangement property"""
        return self.properties.get("searchEnableAutomaticIndexSizeManangement", None)

    @odata(name="searchEnableRemoteQueries")
    @property
    def search_enable_remote_queries(self) -> Optional[bool]:
        """Gets the searchEnableRemoteQueries property"""
        return self.properties.get("searchEnableRemoteQueries", None)

    @odata(name="settingsBlockAccountsPage")
    @property
    def settings_block_accounts_page(self) -> Optional[bool]:
        """Gets the settingsBlockAccountsPage property"""
        return self.properties.get("settingsBlockAccountsPage", None)

    @odata(name="settingsBlockAddProvisioningPackage")
    @property
    def settings_block_add_provisioning_package(self) -> Optional[bool]:
        """Gets the settingsBlockAddProvisioningPackage property"""
        return self.properties.get("settingsBlockAddProvisioningPackage", None)

    @odata(name="settingsBlockAppsPage")
    @property
    def settings_block_apps_page(self) -> Optional[bool]:
        """Gets the settingsBlockAppsPage property"""
        return self.properties.get("settingsBlockAppsPage", None)

    @odata(name="settingsBlockChangeLanguage")
    @property
    def settings_block_change_language(self) -> Optional[bool]:
        """Gets the settingsBlockChangeLanguage property"""
        return self.properties.get("settingsBlockChangeLanguage", None)

    @odata(name="settingsBlockChangePowerSleep")
    @property
    def settings_block_change_power_sleep(self) -> Optional[bool]:
        """Gets the settingsBlockChangePowerSleep property"""
        return self.properties.get("settingsBlockChangePowerSleep", None)

    @odata(name="settingsBlockChangeRegion")
    @property
    def settings_block_change_region(self) -> Optional[bool]:
        """Gets the settingsBlockChangeRegion property"""
        return self.properties.get("settingsBlockChangeRegion", None)

    @odata(name="settingsBlockChangeSystemTime")
    @property
    def settings_block_change_system_time(self) -> Optional[bool]:
        """Gets the settingsBlockChangeSystemTime property"""
        return self.properties.get("settingsBlockChangeSystemTime", None)

    @odata(name="settingsBlockDevicesPage")
    @property
    def settings_block_devices_page(self) -> Optional[bool]:
        """Gets the settingsBlockDevicesPage property"""
        return self.properties.get("settingsBlockDevicesPage", None)

    @odata(name="settingsBlockEaseOfAccessPage")
    @property
    def settings_block_ease_of_access_page(self) -> Optional[bool]:
        """Gets the settingsBlockEaseOfAccessPage property"""
        return self.properties.get("settingsBlockEaseOfAccessPage", None)

    @odata(name="settingsBlockEditDeviceName")
    @property
    def settings_block_edit_device_name(self) -> Optional[bool]:
        """Gets the settingsBlockEditDeviceName property"""
        return self.properties.get("settingsBlockEditDeviceName", None)

    @odata(name="settingsBlockGamingPage")
    @property
    def settings_block_gaming_page(self) -> Optional[bool]:
        """Gets the settingsBlockGamingPage property"""
        return self.properties.get("settingsBlockGamingPage", None)

    @odata(name="settingsBlockNetworkInternetPage")
    @property
    def settings_block_network_internet_page(self) -> Optional[bool]:
        """Gets the settingsBlockNetworkInternetPage property"""
        return self.properties.get("settingsBlockNetworkInternetPage", None)

    @odata(name="settingsBlockPersonalizationPage")
    @property
    def settings_block_personalization_page(self) -> Optional[bool]:
        """Gets the settingsBlockPersonalizationPage property"""
        return self.properties.get("settingsBlockPersonalizationPage", None)

    @odata(name="settingsBlockPrivacyPage")
    @property
    def settings_block_privacy_page(self) -> Optional[bool]:
        """Gets the settingsBlockPrivacyPage property"""
        return self.properties.get("settingsBlockPrivacyPage", None)

    @odata(name="settingsBlockRemoveProvisioningPackage")
    @property
    def settings_block_remove_provisioning_package(self) -> Optional[bool]:
        """Gets the settingsBlockRemoveProvisioningPackage property"""
        return self.properties.get("settingsBlockRemoveProvisioningPackage", None)

    @odata(name="settingsBlockSettingsApp")
    @property
    def settings_block_settings_app(self) -> Optional[bool]:
        """Gets the settingsBlockSettingsApp property"""
        return self.properties.get("settingsBlockSettingsApp", None)

    @odata(name="settingsBlockSystemPage")
    @property
    def settings_block_system_page(self) -> Optional[bool]:
        """Gets the settingsBlockSystemPage property"""
        return self.properties.get("settingsBlockSystemPage", None)

    @odata(name="settingsBlockTimeLanguagePage")
    @property
    def settings_block_time_language_page(self) -> Optional[bool]:
        """Gets the settingsBlockTimeLanguagePage property"""
        return self.properties.get("settingsBlockTimeLanguagePage", None)

    @odata(name="settingsBlockUpdateSecurityPage")
    @property
    def settings_block_update_security_page(self) -> Optional[bool]:
        """Gets the settingsBlockUpdateSecurityPage property"""
        return self.properties.get("settingsBlockUpdateSecurityPage", None)

    @odata(name="sharedUserAppDataAllowed")
    @property
    def shared_user_app_data_allowed(self) -> Optional[bool]:
        """Gets the sharedUserAppDataAllowed property"""
        return self.properties.get("sharedUserAppDataAllowed", None)

    @odata(name="smartScreenBlockPromptOverride")
    @property
    def smart_screen_block_prompt_override(self) -> Optional[bool]:
        """Gets the smartScreenBlockPromptOverride property"""
        return self.properties.get("smartScreenBlockPromptOverride", None)

    @odata(name="smartScreenBlockPromptOverrideForFiles")
    @property
    def smart_screen_block_prompt_override_for_files(self) -> Optional[bool]:
        """Gets the smartScreenBlockPromptOverrideForFiles property"""
        return self.properties.get("smartScreenBlockPromptOverrideForFiles", None)

    @odata(name="smartScreenEnableAppInstallControl")
    @property
    def smart_screen_enable_app_install_control(self) -> Optional[bool]:
        """Gets the smartScreenEnableAppInstallControl property"""
        return self.properties.get("smartScreenEnableAppInstallControl", None)

    @odata(name="startBlockUnpinningAppsFromTaskbar")
    @property
    def start_block_unpinning_apps_from_taskbar(self) -> Optional[bool]:
        """Gets the startBlockUnpinningAppsFromTaskbar property"""
        return self.properties.get("startBlockUnpinningAppsFromTaskbar", None)

    @odata(name="startMenuAppListVisibility")
    @property
    def start_menu_app_list_visibility(self) -> WindowsStartMenuAppListVisibilityType:
        """Gets the startMenuAppListVisibility property"""
        return self.properties.get("startMenuAppListVisibility", WindowsStartMenuAppListVisibilityType.userDefined)

    @odata(name="startMenuHideChangeAccountSettings")
    @property
    def start_menu_hide_change_account_settings(self) -> Optional[bool]:
        """Gets the startMenuHideChangeAccountSettings property"""
        return self.properties.get("startMenuHideChangeAccountSettings", None)

    @odata(name="startMenuHideFrequentlyUsedApps")
    @property
    def start_menu_hide_frequently_used_apps(self) -> Optional[bool]:
        """Gets the startMenuHideFrequentlyUsedApps property"""
        return self.properties.get("startMenuHideFrequentlyUsedApps", None)

    @odata(name="startMenuHideHibernate")
    @property
    def start_menu_hide_hibernate(self) -> Optional[bool]:
        """Gets the startMenuHideHibernate property"""
        return self.properties.get("startMenuHideHibernate", None)

    @odata(name="startMenuHideLock")
    @property
    def start_menu_hide_lock(self) -> Optional[bool]:
        """Gets the startMenuHideLock property"""
        return self.properties.get("startMenuHideLock", None)

    @odata(name="startMenuHidePowerButton")
    @property
    def start_menu_hide_power_button(self) -> Optional[bool]:
        """Gets the startMenuHidePowerButton property"""
        return self.properties.get("startMenuHidePowerButton", None)

    @odata(name="startMenuHideRecentJumpLists")
    @property
    def start_menu_hide_recent_jump_lists(self) -> Optional[bool]:
        """Gets the startMenuHideRecentJumpLists property"""
        return self.properties.get("startMenuHideRecentJumpLists", None)

    @odata(name="startMenuHideRecentlyAddedApps")
    @property
    def start_menu_hide_recently_added_apps(self) -> Optional[bool]:
        """Gets the startMenuHideRecentlyAddedApps property"""
        return self.properties.get("startMenuHideRecentlyAddedApps", None)

    @odata(name="startMenuHideRestartOptions")
    @property
    def start_menu_hide_restart_options(self) -> Optional[bool]:
        """Gets the startMenuHideRestartOptions property"""
        return self.properties.get("startMenuHideRestartOptions", None)

    @odata(name="startMenuHideShutDown")
    @property
    def start_menu_hide_shut_down(self) -> Optional[bool]:
        """Gets the startMenuHideShutDown property"""
        return self.properties.get("startMenuHideShutDown", None)

    @odata(name="startMenuHideSignOut")
    @property
    def start_menu_hide_sign_out(self) -> Optional[bool]:
        """Gets the startMenuHideSignOut property"""
        return self.properties.get("startMenuHideSignOut", None)

    @odata(name="startMenuHideSleep")
    @property
    def start_menu_hide_sleep(self) -> Optional[bool]:
        """Gets the startMenuHideSleep property"""
        return self.properties.get("startMenuHideSleep", None)

    @odata(name="startMenuHideSwitchAccount")
    @property
    def start_menu_hide_switch_account(self) -> Optional[bool]:
        """Gets the startMenuHideSwitchAccount property"""
        return self.properties.get("startMenuHideSwitchAccount", None)

    @odata(name="startMenuHideUserTile")
    @property
    def start_menu_hide_user_tile(self) -> Optional[bool]:
        """Gets the startMenuHideUserTile property"""
        return self.properties.get("startMenuHideUserTile", None)

    @odata(name="startMenuLayoutEdgeAssetsXml")
    @property
    def start_menu_layout_edge_assets_xml(self) -> Optional[bytes]:
        """Gets the startMenuLayoutEdgeAssetsXml property"""
        return self.properties.get("startMenuLayoutEdgeAssetsXml", None)

    @odata(name="startMenuLayoutXml")
    @property
    def start_menu_layout_xml(self) -> Optional[bytes]:
        """Gets the startMenuLayoutXml property"""
        return self.properties.get("startMenuLayoutXml", None)

    @odata(name="startMenuMode")
    @property
    def start_menu_mode(self) -> WindowsStartMenuModeType:
        """Gets the startMenuMode property"""
        return self.properties.get("startMenuMode", WindowsStartMenuModeType.userDefined)

    @odata(name="startMenuPinnedFolderDocuments")
    @property
    def start_menu_pinned_folder_documents(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderDocuments property"""
        return self.properties.get("startMenuPinnedFolderDocuments", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderDownloads")
    @property
    def start_menu_pinned_folder_downloads(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderDownloads property"""
        return self.properties.get("startMenuPinnedFolderDownloads", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderFileExplorer")
    @property
    def start_menu_pinned_folder_file_explorer(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderFileExplorer property"""
        return self.properties.get("startMenuPinnedFolderFileExplorer", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderHomeGroup")
    @property
    def start_menu_pinned_folder_home_group(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderHomeGroup property"""
        return self.properties.get("startMenuPinnedFolderHomeGroup", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderMusic")
    @property
    def start_menu_pinned_folder_music(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderMusic property"""
        return self.properties.get("startMenuPinnedFolderMusic", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderNetwork")
    @property
    def start_menu_pinned_folder_network(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderNetwork property"""
        return self.properties.get("startMenuPinnedFolderNetwork", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderPersonalFolder")
    @property
    def start_menu_pinned_folder_personal_folder(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderPersonalFolder property"""
        return self.properties.get("startMenuPinnedFolderPersonalFolder", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderPictures")
    @property
    def start_menu_pinned_folder_pictures(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderPictures property"""
        return self.properties.get("startMenuPinnedFolderPictures", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderSettings")
    @property
    def start_menu_pinned_folder_settings(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderSettings property"""
        return self.properties.get("startMenuPinnedFolderSettings", VisibilitySetting.notConfigured)

    @odata(name="startMenuPinnedFolderVideos")
    @property
    def start_menu_pinned_folder_videos(self) -> VisibilitySetting:
        """Gets the startMenuPinnedFolderVideos property"""
        return self.properties.get("startMenuPinnedFolderVideos", VisibilitySetting.notConfigured)

    @odata(name="storageBlockRemovableStorage")
    @property
    def storage_block_removable_storage(self) -> Optional[bool]:
        """Gets the storageBlockRemovableStorage property"""
        return self.properties.get("storageBlockRemovableStorage", None)

    @odata(name="storageRequireMobileDeviceEncryption")
    @property
    def storage_require_mobile_device_encryption(self) -> Optional[bool]:
        """Gets the storageRequireMobileDeviceEncryption property"""
        return self.properties.get("storageRequireMobileDeviceEncryption", None)

    @odata(name="storageRestrictAppDataToSystemVolume")
    @property
    def storage_restrict_app_data_to_system_volume(self) -> Optional[bool]:
        """Gets the storageRestrictAppDataToSystemVolume property"""
        return self.properties.get("storageRestrictAppDataToSystemVolume", None)

    @odata(name="storageRestrictAppInstallToSystemVolume")
    @property
    def storage_restrict_app_install_to_system_volume(self) -> Optional[bool]:
        """Gets the storageRestrictAppInstallToSystemVolume property"""
        return self.properties.get("storageRestrictAppInstallToSystemVolume", None)

    @odata(name="tenantLockdownRequireNetworkDuringOutOfBoxExperience")
    @property
    def tenant_lockdown_require_network_during_out_of_box_experience(self) -> Optional[bool]:
        """Gets the tenantLockdownRequireNetworkDuringOutOfBoxExperience property"""
        return self.properties.get("tenantLockdownRequireNetworkDuringOutOfBoxExperience", None)

    @odata(name="usbBlocked")
    @property
    def usb_blocked(self) -> Optional[bool]:
        """Gets the usbBlocked property"""
        return self.properties.get("usbBlocked", None)

    @odata(name="voiceRecordingBlocked")
    @property
    def voice_recording_blocked(self) -> Optional[bool]:
        """Gets the voiceRecordingBlocked property"""
        return self.properties.get("voiceRecordingBlocked", None)

    @odata(name="webRtcBlockLocalhostIpAddress")
    @property
    def web_rtc_block_localhost_ip_address(self) -> Optional[bool]:
        """Gets the webRtcBlockLocalhostIpAddress property"""
        return self.properties.get("webRtcBlockLocalhostIpAddress", None)

    @odata(name="wiFiBlockAutomaticConnectHotspots")
    @property
    def wi_fi_block_automatic_connect_hotspots(self) -> Optional[bool]:
        """Gets the wiFiBlockAutomaticConnectHotspots property"""
        return self.properties.get("wiFiBlockAutomaticConnectHotspots", None)

    @odata(name="wiFiBlocked")
    @property
    def wi_fi_blocked(self) -> Optional[bool]:
        """Gets the wiFiBlocked property"""
        return self.properties.get("wiFiBlocked", None)

    @odata(name="wiFiBlockManualConfiguration")
    @property
    def wi_fi_block_manual_configuration(self) -> Optional[bool]:
        """Gets the wiFiBlockManualConfiguration property"""
        return self.properties.get("wiFiBlockManualConfiguration", None)

    @odata(name="wiFiScanInterval")
    @property
    def wi_fi_scan_interval(self) -> Optional[int]:
        """Gets the wiFiScanInterval property"""
        return self.properties.get("wiFiScanInterval", None)

    @odata(name="windowsSpotlightBlockConsumerSpecificFeatures")
    @property
    def windows_spotlight_block_consumer_specific_features(self) -> Optional[bool]:
        """Gets the windowsSpotlightBlockConsumerSpecificFeatures property"""
        return self.properties.get("windowsSpotlightBlockConsumerSpecificFeatures", None)

    @odata(name="windowsSpotlightBlocked")
    @property
    def windows_spotlight_blocked(self) -> Optional[bool]:
        """Gets the windowsSpotlightBlocked property"""
        return self.properties.get("windowsSpotlightBlocked", None)

    @odata(name="windowsSpotlightBlockOnActionCenter")
    @property
    def windows_spotlight_block_on_action_center(self) -> Optional[bool]:
        """Gets the windowsSpotlightBlockOnActionCenter property"""
        return self.properties.get("windowsSpotlightBlockOnActionCenter", None)

    @odata(name="windowsSpotlightBlockTailoredExperiences")
    @property
    def windows_spotlight_block_tailored_experiences(self) -> Optional[bool]:
        """Gets the windowsSpotlightBlockTailoredExperiences property"""
        return self.properties.get("windowsSpotlightBlockTailoredExperiences", None)

    @odata(name="windowsSpotlightBlockThirdPartyNotifications")
    @property
    def windows_spotlight_block_third_party_notifications(self) -> Optional[bool]:
        """Gets the windowsSpotlightBlockThirdPartyNotifications property"""
        return self.properties.get("windowsSpotlightBlockThirdPartyNotifications", None)

    @odata(name="windowsSpotlightBlockWelcomeExperience")
    @property
    def windows_spotlight_block_welcome_experience(self) -> Optional[bool]:
        """Gets the windowsSpotlightBlockWelcomeExperience property"""
        return self.properties.get("windowsSpotlightBlockWelcomeExperience", None)

    @odata(name="windowsSpotlightBlockWindowsTips")
    @property
    def windows_spotlight_block_windows_tips(self) -> Optional[bool]:
        """Gets the windowsSpotlightBlockWindowsTips property"""
        return self.properties.get("windowsSpotlightBlockWindowsTips", None)

    @odata(name="windowsSpotlightConfigureOnLockScreen")
    @property
    def windows_spotlight_configure_on_lock_screen(self) -> WindowsSpotlightEnablementSettings:
        """Gets the windowsSpotlightConfigureOnLockScreen property"""
        return self.properties.get(
            "windowsSpotlightConfigureOnLockScreen", WindowsSpotlightEnablementSettings.notConfigured
        )

    @odata(name="windowsStoreBlockAutoUpdate")
    @property
    def windows_store_block_auto_update(self) -> Optional[bool]:
        """Gets the windowsStoreBlockAutoUpdate property"""
        return self.properties.get("windowsStoreBlockAutoUpdate", None)

    @odata(name="windowsStoreBlocked")
    @property
    def windows_store_blocked(self) -> Optional[bool]:
        """Gets the windowsStoreBlocked property"""
        return self.properties.get("windowsStoreBlocked", None)

    @odata(name="windowsStoreEnablePrivateStoreOnly")
    @property
    def windows_store_enable_private_store_only(self) -> Optional[bool]:
        """Gets the windowsStoreEnablePrivateStoreOnly property"""
        return self.properties.get("windowsStoreEnablePrivateStoreOnly", None)

    @odata(name="wirelessDisplayBlockProjectionToThisDevice")
    @property
    def wireless_display_block_projection_to_this_device(self) -> Optional[bool]:
        """Gets the wirelessDisplayBlockProjectionToThisDevice property"""
        return self.properties.get("wirelessDisplayBlockProjectionToThisDevice", None)

    @odata(name="wirelessDisplayBlockUserInputFromReceiver")
    @property
    def wireless_display_block_user_input_from_receiver(self) -> Optional[bool]:
        """Gets the wirelessDisplayBlockUserInputFromReceiver property"""
        return self.properties.get("wirelessDisplayBlockUserInputFromReceiver", None)

    @odata(name="wirelessDisplayRequirePinForPairing")
    @property
    def wireless_display_require_pin_for_pairing(self) -> Optional[bool]:
        """Gets the wirelessDisplayRequirePinForPairing property"""
        return self.properties.get("wirelessDisplayRequirePinForPairing", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows10GeneralConfiguration"
