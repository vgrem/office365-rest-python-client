from __future__ import annotations

from enum import Enum


class BrowseQueryResponseItemType(Enum):
    none = "0"
    site = "1"
    documentLibrary = "2"
    folder = "3"
    file = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowseQueryResponseItemType"
