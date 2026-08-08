from __future__ import annotations

from enum import Enum


class BrowsableResourceType(Enum):
    none = "0"
    site = "1"
    documentLibrary = "2"
    folder = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowsableResourceType"
