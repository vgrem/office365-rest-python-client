from __future__ import annotations

from enum import Enum


class TimeCardState(Enum):
    clockedIn = "0"
    onBreak = "1"
    clockedOut = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeCardState"
