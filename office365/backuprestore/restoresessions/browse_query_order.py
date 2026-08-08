from __future__ import annotations

from enum import Enum


class BrowseQueryOrder(Enum):
    pathAsc = "0"
    pathDsc = "1"
    nameAsc = "2"
    nameDsc = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowseQueryOrder"
