from __future__ import annotations

from office365.runtime.client_value import ClientValue


class UserInactivityTrigger(ClientValue):
    inactivityPeriodInDays: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.UserInactivityTrigger"
