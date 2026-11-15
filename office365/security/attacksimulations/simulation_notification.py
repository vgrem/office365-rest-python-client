from __future__ import annotations

from office365.security.attacksimulations.base_end_user_notification import BaseEndUserNotification
from office365.security.attacksimulations.targettedusertype import (
    TargettedUserType,
)


class SimulationNotification(BaseEndUserNotification):
    targettedUserType: TargettedUserType = TargettedUserType.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SimulationNotification"
