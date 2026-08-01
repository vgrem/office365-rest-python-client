from __future__ import annotations

from enum import Enum


class ContentCategory(Enum):
    none = "0"
    ai = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ContentCategory"
