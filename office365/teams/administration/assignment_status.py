from __future__ import annotations

from enum import Enum


class AssignmentStatus(Enum):
    unassigned = "0"
    internalError = "1"
    userAssigned = "2"
    conferenceAssigned = "3"
    voiceApplicationAssigned = "4"
    thirdPartyAppAssigned = "5"
    policyAssigned = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.AssignmentStatus"
