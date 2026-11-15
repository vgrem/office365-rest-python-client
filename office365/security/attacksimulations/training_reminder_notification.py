from __future__ import annotations

from office365.security.attacksimulations.base_end_user_notification import BaseEndUserNotification
from office365.security.attacksimulations.notificationdeliveryfrequency import (
    NotificationDeliveryFrequency,
)


class TrainingReminderNotification(BaseEndUserNotification):
    deliveryFrequency: NotificationDeliveryFrequency = NotificationDeliveryFrequency.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TrainingReminderNotification"
