from __future__ import annotations

from enum import Enum


class GroupAccessType(Enum):
    none = "0"
    private = "1"
    secret = "2"
    public = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupAccessType"
