from __future__ import annotations

from office365.security.attacksimulations.targettedusertype import (
    TargettedUserType,
)
from office365.security.base_end_user_notification import BaseEndUserNotification


class SimulationNotification(BaseEndUserNotification):
    targettedUserType: TargettedUserType = TargettedUserType.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SimulationNotification"
