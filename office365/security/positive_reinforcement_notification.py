from __future__ import annotations

from office365.security.attacksimulations.notificationdeliverypreference import (
    NotificationDeliveryPreference,
)
from office365.security.base_end_user_notification import BaseEndUserNotification


class PositiveReinforcementNotification(BaseEndUserNotification):
    deliveryPreference: NotificationDeliveryPreference = NotificationDeliveryPreference.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PositiveReinforcementNotification"
