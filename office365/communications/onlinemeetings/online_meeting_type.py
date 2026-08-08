from __future__ import annotations

from enum import Enum


class OnlineMeetingType(Enum):
    adhoc = "0"
    scheduled = "1"
    recurring = "2"
    broadcast = "3"
    meetnow = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnlineMeetingType"
