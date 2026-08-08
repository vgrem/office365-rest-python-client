from __future__ import annotations

from enum import Enum


class WorkLocationSource(Enum):
    none = "0"
    manual = "1"
    scheduled = "2"
    automatic = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkLocationSource"
