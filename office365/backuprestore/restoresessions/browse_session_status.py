from __future__ import annotations

from enum import Enum


class BrowseSessionStatus(Enum):
    creating = "0"
    created = "1"
    failed = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowseSessionStatus"
