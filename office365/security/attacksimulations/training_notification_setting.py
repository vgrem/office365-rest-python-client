from __future__ import annotations

from dataclasses import field

from office365.security.attacksimulations.base_end_user_notification import (
    BaseEndUserNotification,
)
from office365.security.attacksimulations.end_user_notification_setting import EndUserNotificationSetting
from office365.security.attacksimulations.training_reminder_notification import (
    TrainingReminderNotification,
)


class TrainingNotificationSetting(EndUserNotificationSetting):
    trainingAssignment: BaseEndUserNotification = field(default_factory=BaseEndUserNotification)
    trainingReminder: TrainingReminderNotification = field(default_factory=TrainingReminderNotification)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TrainingNotificationSetting"
