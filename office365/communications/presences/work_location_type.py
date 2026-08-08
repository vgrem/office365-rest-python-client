from __future__ import annotations

from enum import Enum


class WorkLocationType(Enum):
    unspecified = "0"
    office = "1"
    remote = "2"
    timeOff = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkLocationType"
