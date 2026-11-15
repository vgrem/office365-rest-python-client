from __future__ import annotations

from enum import Enum


class MeetingEngagementType(Enum):
    reaction = "0"
    hand = "1"
    camera = "2"
    microphone = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MeetingEngagementType"
