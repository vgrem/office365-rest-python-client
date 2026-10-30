from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.configurations.windows.miracastchannel import (
        MiracastChannel,
    )
    from office365.intune.devices.configurations.windows.welcomescreenmeetinginformation import (
        WelcomeScreenMeetingInformation,
    )


class Windows10TeamGeneralConfiguration(Entity):
    @odata(name="azureOperationalInsightsBlockTelemetry")
    @property
    def azure_operational_insights_block_telemetry(self) -> Optional[bool]:
        """Gets the azureOperationalInsightsBlockTelemetry property"""
        return self.properties.get("azureOperationalInsightsBlockTelemetry", None)

    @odata(name="azureOperationalInsightsWorkspaceId")
    @property
    def azure_operational_insights_workspace_id(self) -> Optional[str]:
        """Gets the azureOperationalInsightsWorkspaceId property"""
        return self.properties.get("azureOperationalInsightsWorkspaceId", None)

    @odata(name="azureOperationalInsightsWorkspaceKey")
    @property
    def azure_operational_insights_workspace_key(self) -> Optional[str]:
        """Gets the azureOperationalInsightsWorkspaceKey property"""
        return self.properties.get("azureOperationalInsightsWorkspaceKey", None)

    @odata(name="connectAppBlockAutoLaunch")
    @property
    def connect_app_block_auto_launch(self) -> Optional[bool]:
        """Gets the connectAppBlockAutoLaunch property"""
        return self.properties.get("connectAppBlockAutoLaunch", None)

    @odata(name="maintenanceWindowBlocked")
    @property
    def maintenance_window_blocked(self) -> Optional[bool]:
        """Gets the maintenanceWindowBlocked property"""
        return self.properties.get("maintenanceWindowBlocked", None)

    @odata(name="maintenanceWindowDurationInHours")
    @property
    def maintenance_window_duration_in_hours(self) -> Optional[int]:
        """Gets the maintenanceWindowDurationInHours property"""
        return self.properties.get("maintenanceWindowDurationInHours", None)

    @odata(name="maintenanceWindowStartTime")
    @property
    def maintenance_window_start_time(self) -> Optional[time]:
        """Gets the maintenanceWindowStartTime property"""
        return self.properties.get("maintenanceWindowStartTime", None)

    @odata(name="miracastBlocked")
    @property
    def miracast_blocked(self) -> Optional[bool]:
        """Gets the miracastBlocked property"""
        return self.properties.get("miracastBlocked", None)

    @odata(name="miracastChannel")
    @property
    def miracast_channel(self) -> MiracastChannel:
        """Gets the miracastChannel property"""
        from office365.intune.devices.configurations.windows.miracastchannel import (
            MiracastChannel,
        )

        return self.properties.get("miracastChannel", MiracastChannel.userDefined)

    @odata(name="miracastRequirePin")
    @property
    def miracast_require_pin(self) -> Optional[bool]:
        """Gets the miracastRequirePin property"""
        return self.properties.get("miracastRequirePin", None)

    @odata(name="settingsBlockMyMeetingsAndFiles")
    @property
    def settings_block_my_meetings_and_files(self) -> Optional[bool]:
        """Gets the settingsBlockMyMeetingsAndFiles property"""
        return self.properties.get("settingsBlockMyMeetingsAndFiles", None)

    @odata(name="settingsBlockSessionResume")
    @property
    def settings_block_session_resume(self) -> Optional[bool]:
        """Gets the settingsBlockSessionResume property"""
        return self.properties.get("settingsBlockSessionResume", None)

    @odata(name="settingsBlockSigninSuggestions")
    @property
    def settings_block_signin_suggestions(self) -> Optional[bool]:
        """Gets the settingsBlockSigninSuggestions property"""
        return self.properties.get("settingsBlockSigninSuggestions", None)

    @odata(name="settingsDefaultVolume")
    @property
    def settings_default_volume(self) -> Optional[int]:
        """Gets the settingsDefaultVolume property"""
        return self.properties.get("settingsDefaultVolume", None)

    @odata(name="settingsScreenTimeoutInMinutes")
    @property
    def settings_screen_timeout_in_minutes(self) -> Optional[int]:
        """Gets the settingsScreenTimeoutInMinutes property"""
        return self.properties.get("settingsScreenTimeoutInMinutes", None)

    @odata(name="settingsSessionTimeoutInMinutes")
    @property
    def settings_session_timeout_in_minutes(self) -> Optional[int]:
        """Gets the settingsSessionTimeoutInMinutes property"""
        return self.properties.get("settingsSessionTimeoutInMinutes", None)

    @odata(name="settingsSleepTimeoutInMinutes")
    @property
    def settings_sleep_timeout_in_minutes(self) -> Optional[int]:
        """Gets the settingsSleepTimeoutInMinutes property"""
        return self.properties.get("settingsSleepTimeoutInMinutes", None)

    @odata(name="welcomeScreenBackgroundImageUrl")
    @property
    def welcome_screen_background_image_url(self) -> Optional[str]:
        """Gets the welcomeScreenBackgroundImageUrl property"""
        return self.properties.get("welcomeScreenBackgroundImageUrl", None)

    @odata(name="welcomeScreenBlockAutomaticWakeUp")
    @property
    def welcome_screen_block_automatic_wake_up(self) -> Optional[bool]:
        """Gets the welcomeScreenBlockAutomaticWakeUp property"""
        return self.properties.get("welcomeScreenBlockAutomaticWakeUp", None)

    @odata(name="welcomeScreenMeetingInformation")
    @property
    def welcome_screen_meeting_information(self) -> WelcomeScreenMeetingInformation:
        """Gets the welcomeScreenMeetingInformation property"""
        from office365.intune.devices.configurations.windows.welcomescreenmeetinginformation import (
            WelcomeScreenMeetingInformation,
        )

        return self.properties.get("welcomeScreenMeetingInformation", WelcomeScreenMeetingInformation.userDefined)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows10TeamGeneralConfiguration"
