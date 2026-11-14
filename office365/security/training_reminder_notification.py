from __future__ import annotations

from office365.security.attacksimulations.notificationdeliveryfrequency import (
    NotificationDeliveryFrequency,
)
from office365.security.base_end_user_notification import BaseEndUserNotification


class TrainingReminderNotification(BaseEndUserNotification):
    deliveryFrequency: NotificationDeliveryFrequency = NotificationDeliveryFrequency.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TrainingReminderNotification"
