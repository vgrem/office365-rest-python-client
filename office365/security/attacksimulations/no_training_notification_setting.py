from __future__ import annotations

from dataclasses import field

from office365.security.attacksimulations.end_user_notification_setting import EndUserNotificationSetting
from office365.security.attacksimulations.simulation_notification import SimulationNotification


class NoTrainingNotificationSetting(EndUserNotificationSetting):
    simulationNotification: SimulationNotification = field(default_factory=SimulationNotification)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.NoTrainingNotificationSetting"
