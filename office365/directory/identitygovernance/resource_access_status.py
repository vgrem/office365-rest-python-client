from __future__ import annotations

from enum import Enum


class ResourceAccessStatus(Enum):
    none = "0"
    failure = "1"
    success = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResourceAccessStatus"
