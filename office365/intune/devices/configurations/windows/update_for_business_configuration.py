from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.configurations.enablement import Enablement
    from office365.intune.devices.configurations.windows.automaticupdatemode import (
        AutomaticUpdateMode,
    )
    from office365.intune.devices.configurations.windows.autorestartnotificationdismissalmethod import (
        AutoRestartNotificationDismissalMethod,
    )
    from office365.intune.devices.configurations.windows.deliveryoptimizationmode import (
        WindowsDeliveryOptimizationMode,
    )
    from office365.intune.devices.configurations.windows.prereleasefeatures import (
        PrereleaseFeatures,
    )
    from office365.intune.devices.configurations.windows.update_install_schedule_type import (
        WindowsUpdateInstallScheduleType,
    )
    from office365.intune.devices.configurations.windows.updateforbusinessupdateweeks import (
        WindowsUpdateForBusinessUpdateWeeks,
    )
    from office365.intune.devices.configurations.windows.updatenotificationdisplayoption import (
        WindowsUpdateNotificationDisplayOption,
    )
    from office365.intune.devices.configurations.windows.updatetype import (
        WindowsUpdateType,
    )


class WindowsUpdateForBusinessConfiguration(Entity):
    @odata(name="allowWindows11Upgrade")
    @property
    def allow_windows11_upgrade(self) -> Optional[bool]:
        """Gets the allowWindows11Upgrade property"""
        return self.properties.get("allowWindows11Upgrade", None)

    @odata(name="automaticUpdateMode")
    @property
    def automatic_update_mode(self) -> AutomaticUpdateMode:
        """Gets the automaticUpdateMode property"""
        from office365.intune.devices.configurations.windows.automaticupdatemode import (
            AutomaticUpdateMode,
        )

        return self.properties.get("automaticUpdateMode", AutomaticUpdateMode.userDefined)

    @odata(name="autoRestartNotificationDismissal")
    @property
    def auto_restart_notification_dismissal(self) -> AutoRestartNotificationDismissalMethod:
        """Gets the autoRestartNotificationDismissal property"""
        from office365.intune.devices.configurations.windows.autorestartnotificationdismissalmethod import (
            AutoRestartNotificationDismissalMethod,
        )

        return self.properties.get(
            "autoRestartNotificationDismissal", AutoRestartNotificationDismissalMethod.notConfigured
        )

    @odata(name="businessReadyUpdatesOnly")
    @property
    def business_ready_updates_only(self) -> WindowsUpdateType:
        """Gets the businessReadyUpdatesOnly property"""
        from office365.intune.devices.configurations.windows.updatetype import (
            WindowsUpdateType,
        )

        return self.properties.get("businessReadyUpdatesOnly", WindowsUpdateType.userDefined)

    @odata(name="deadlineForFeatureUpdatesInDays")
    @property
    def deadline_for_feature_updates_in_days(self) -> Optional[int]:
        """Gets the deadlineForFeatureUpdatesInDays property"""
        return self.properties.get("deadlineForFeatureUpdatesInDays", None)

    @odata(name="deadlineForQualityUpdatesInDays")
    @property
    def deadline_for_quality_updates_in_days(self) -> Optional[int]:
        """Gets the deadlineForQualityUpdatesInDays property"""
        return self.properties.get("deadlineForQualityUpdatesInDays", None)

    @odata(name="deadlineGracePeriodInDays")
    @property
    def deadline_grace_period_in_days(self) -> Optional[int]:
        """Gets the deadlineGracePeriodInDays property"""
        return self.properties.get("deadlineGracePeriodInDays", None)

    @odata(name="deliveryOptimizationMode")
    @property
    def delivery_optimization_mode(self) -> WindowsDeliveryOptimizationMode:
        """Gets the deliveryOptimizationMode property"""
        from office365.intune.devices.configurations.windows.deliveryoptimizationmode import (
            WindowsDeliveryOptimizationMode,
        )

        return self.properties.get("deliveryOptimizationMode", WindowsDeliveryOptimizationMode.userDefined)

    @odata(name="driversExcluded")
    @property
    def drivers_excluded(self) -> Optional[bool]:
        """Gets the driversExcluded property"""
        return self.properties.get("driversExcluded", None)

    @odata(name="engagedRestartDeadlineInDays")
    @property
    def engaged_restart_deadline_in_days(self) -> Optional[int]:
        """Gets the engagedRestartDeadlineInDays property"""
        return self.properties.get("engagedRestartDeadlineInDays", None)

    @odata(name="engagedRestartSnoozeScheduleInDays")
    @property
    def engaged_restart_snooze_schedule_in_days(self) -> Optional[int]:
        """Gets the engagedRestartSnoozeScheduleInDays property"""
        return self.properties.get("engagedRestartSnoozeScheduleInDays", None)

    @odata(name="engagedRestartTransitionScheduleInDays")
    @property
    def engaged_restart_transition_schedule_in_days(self) -> Optional[int]:
        """Gets the engagedRestartTransitionScheduleInDays property"""
        return self.properties.get("engagedRestartTransitionScheduleInDays", None)

    @odata(name="featureUpdatesDeferralPeriodInDays")
    @property
    def feature_updates_deferral_period_in_days(self) -> Optional[int]:
        """Gets the featureUpdatesDeferralPeriodInDays property"""
        return self.properties.get("featureUpdatesDeferralPeriodInDays", None)

    @odata(name="featureUpdatesPaused")
    @property
    def feature_updates_paused(self) -> Optional[bool]:
        """Gets the featureUpdatesPaused property"""
        return self.properties.get("featureUpdatesPaused", None)

    @odata(name="featureUpdatesPauseExpiryDateTime")
    @property
    def feature_updates_pause_expiry_date_time(self) -> Optional[datetime]:
        """Gets the featureUpdatesPauseExpiryDateTime property"""
        return self.properties.get("featureUpdatesPauseExpiryDateTime", datetime.min)

    @odata(name="featureUpdatesPauseStartDate", readonly=True)
    @property
    def feature_updates_pause_start_date(self) -> Optional[date]:
        """Gets the featureUpdatesPauseStartDate property"""
        return self.properties.get("featureUpdatesPauseStartDate", None)

    @odata(name="featureUpdatesRollbackStartDateTime")
    @property
    def feature_updates_rollback_start_date_time(self) -> Optional[datetime]:
        """Gets the featureUpdatesRollbackStartDateTime property"""
        return self.properties.get("featureUpdatesRollbackStartDateTime", datetime.min)

    @odata(name="featureUpdatesRollbackWindowInDays")
    @property
    def feature_updates_rollback_window_in_days(self) -> Optional[int]:
        """Gets the featureUpdatesRollbackWindowInDays property"""
        return self.properties.get("featureUpdatesRollbackWindowInDays", None)

    @odata(name="featureUpdatesWillBeRolledBack")
    @property
    def feature_updates_will_be_rolled_back(self) -> Optional[bool]:
        """Gets the featureUpdatesWillBeRolledBack property"""
        return self.properties.get("featureUpdatesWillBeRolledBack", None)

    @odata(name="installationSchedule")
    @property
    def installation_schedule(self) -> Optional[WindowsUpdateInstallScheduleType]:
        """Gets the installationSchedule property"""
        return self.properties.get("installationSchedule", None)

    @odata(name="microsoftUpdateServiceAllowed")
    @property
    def microsoft_update_service_allowed(self) -> Optional[bool]:
        """Gets the microsoftUpdateServiceAllowed property"""
        return self.properties.get("microsoftUpdateServiceAllowed", None)

    @odata(name="postponeRebootUntilAfterDeadline")
    @property
    def postpone_reboot_until_after_deadline(self) -> Optional[bool]:
        """Gets the postponeRebootUntilAfterDeadline property"""
        return self.properties.get("postponeRebootUntilAfterDeadline", None)

    @odata(name="prereleaseFeatures")
    @property
    def prerelease_features(self) -> PrereleaseFeatures:
        """Gets the prereleaseFeatures property"""
        from office365.intune.devices.configurations.windows.prereleasefeatures import (
            PrereleaseFeatures,
        )

        return self.properties.get("prereleaseFeatures", PrereleaseFeatures.userDefined)

    @odata(name="qualityUpdatesDeferralPeriodInDays")
    @property
    def quality_updates_deferral_period_in_days(self) -> Optional[int]:
        """Gets the qualityUpdatesDeferralPeriodInDays property"""
        return self.properties.get("qualityUpdatesDeferralPeriodInDays", None)

    @odata(name="qualityUpdatesPaused")
    @property
    def quality_updates_paused(self) -> Optional[bool]:
        """Gets the qualityUpdatesPaused property"""
        return self.properties.get("qualityUpdatesPaused", None)

    @odata(name="qualityUpdatesPauseExpiryDateTime")
    @property
    def quality_updates_pause_expiry_date_time(self) -> Optional[datetime]:
        """Gets the qualityUpdatesPauseExpiryDateTime property"""
        return self.properties.get("qualityUpdatesPauseExpiryDateTime", datetime.min)

    @odata(name="qualityUpdatesPauseStartDate", readonly=True)
    @property
    def quality_updates_pause_start_date(self) -> Optional[date]:
        """Gets the qualityUpdatesPauseStartDate property"""
        return self.properties.get("qualityUpdatesPauseStartDate", None)

    @odata(name="qualityUpdatesRollbackStartDateTime")
    @property
    def quality_updates_rollback_start_date_time(self) -> Optional[datetime]:
        """Gets the qualityUpdatesRollbackStartDateTime property"""
        return self.properties.get("qualityUpdatesRollbackStartDateTime", datetime.min)

    @odata(name="qualityUpdatesWillBeRolledBack")
    @property
    def quality_updates_will_be_rolled_back(self) -> Optional[bool]:
        """Gets the qualityUpdatesWillBeRolledBack property"""
        return self.properties.get("qualityUpdatesWillBeRolledBack", None)

    @odata(name="scheduleImminentRestartWarningInMinutes")
    @property
    def schedule_imminent_restart_warning_in_minutes(self) -> Optional[int]:
        """Gets the scheduleImminentRestartWarningInMinutes property"""
        return self.properties.get("scheduleImminentRestartWarningInMinutes", None)

    @odata(name="scheduleRestartWarningInHours")
    @property
    def schedule_restart_warning_in_hours(self) -> Optional[int]:
        """Gets the scheduleRestartWarningInHours property"""
        return self.properties.get("scheduleRestartWarningInHours", None)

    @odata(name="skipChecksBeforeRestart")
    @property
    def skip_checks_before_restart(self) -> Optional[bool]:
        """Gets the skipChecksBeforeRestart property"""
        return self.properties.get("skipChecksBeforeRestart", None)

    @odata(name="updateNotificationLevel")
    @property
    def update_notification_level(self) -> WindowsUpdateNotificationDisplayOption:
        """Gets the updateNotificationLevel property"""
        from office365.intune.devices.configurations.windows.updatenotificationdisplayoption import (
            WindowsUpdateNotificationDisplayOption,
        )

        return self.properties.get("updateNotificationLevel", WindowsUpdateNotificationDisplayOption.notConfigured)

    @odata(name="updateWeeks")
    @property
    def update_weeks(self) -> WindowsUpdateForBusinessUpdateWeeks:
        """Gets the updateWeeks property"""
        from office365.intune.devices.configurations.windows.updateforbusinessupdateweeks import (
            WindowsUpdateForBusinessUpdateWeeks,
        )

        return self.properties.get("updateWeeks", WindowsUpdateForBusinessUpdateWeeks.userDefined)

    @odata(name="userPauseAccess")
    @property
    def user_pause_access(self) -> Enablement:
        """Gets the userPauseAccess property"""
        from office365.intune.devices.configurations.enablement import Enablement

        return self.properties.get("userPauseAccess", Enablement.notConfigured)

    @odata(name="userWindowsUpdateScanAccess")
    @property
    def user_windows_update_scan_access(self) -> Enablement:
        """Gets the userWindowsUpdateScanAccess property"""
        from office365.intune.devices.configurations.enablement import Enablement

        return self.properties.get("userWindowsUpdateScanAccess", Enablement.notConfigured)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsUpdateForBusinessConfiguration"
