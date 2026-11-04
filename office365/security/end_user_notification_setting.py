from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.attacksimulations.endusernotificationpreference import (
    EndUserNotificationPreference,
)
from office365.security.attacksimulations.endusernotificationsettingtype import (
    EndUserNotificationSettingType,
)
from office365.security.positive_reinforcement_notification import (
    PositiveReinforcementNotification,
)


@value
class EndUserNotificationSetting(ClientValue):
    notificationPreference: EndUserNotificationPreference = EndUserNotificationPreference.unknown
    positiveReinforcement: PositiveReinforcementNotification = field(default_factory=PositiveReinforcementNotification)
    settingType: EndUserNotificationSettingType = EndUserNotificationSettingType.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EndUserNotificationSetting"
