from __future__ import annotations

from office365.security.attacksimulations.base_end_user_notification import BaseEndUserNotification
from office365.security.attacksimulations.notificationdeliverypreference import (
    NotificationDeliveryPreference,
)


class PositiveReinforcementNotification(BaseEndUserNotification):
    deliveryPreference: NotificationDeliveryPreference = NotificationDeliveryPreference.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PositiveReinforcementNotification"
