from __future__ import annotations

from enum import Enum


class NotifyMembers(Enum):
    all = "0"
    allowSelected = "1"
    blockSelected = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.NotifyMembers"
