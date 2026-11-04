from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.attacksimulations.targettedusertype import (
    TargettedUserType,
)


@value
class SimulationNotification(ClientValue):
    targettedUserType: TargettedUserType = TargettedUserType.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SimulationNotification"
