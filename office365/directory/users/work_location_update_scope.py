from __future__ import annotations

from enum import Enum


class WorkLocationUpdateScope(Enum):
    currentSegment = "1"
    currentDay = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkLocationUpdateScope"
