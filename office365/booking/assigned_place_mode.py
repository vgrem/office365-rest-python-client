from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AssignedPlaceMode(ClientValue):
    assignedUserEmailAddress: str | None = None
    assignedUserId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AssignedPlaceMode"
