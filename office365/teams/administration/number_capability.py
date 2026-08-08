from __future__ import annotations

from enum import Enum


class NumberCapability(Enum):
    conferenceAssignment = "0"
    voiceApplicationAssignment = "1"
    userAssignment = "2"
    teamsPhoneMobile = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.NumberCapability"
