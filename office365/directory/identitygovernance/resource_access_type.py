from __future__ import annotations

from enum import Enum


class ResourceAccessType(Enum):
    none = "0"
    read = "1"
    write = "2"
    create = "4"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResourceAccessType"
