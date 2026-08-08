from __future__ import annotations

from enum import Enum


class RetrievalEntityType(Enum):
    site = "0"
    list = "1"
    listItem = "2"
    drive = "3"
    driveItem = "4"
    externalItem = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RetrievalEntityType"
