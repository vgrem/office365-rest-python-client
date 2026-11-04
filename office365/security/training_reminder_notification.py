from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.attacksimulations.notificationdeliveryfrequency import (
    NotificationDeliveryFrequency,
)


@value
class TrainingReminderNotification(ClientValue):
    deliveryFrequency: NotificationDeliveryFrequency = NotificationDeliveryFrequency.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TrainingReminderNotification"
