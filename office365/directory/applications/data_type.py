from __future__ import annotations

from enum import Enum


class ApplicationDataType(Enum):
    none = "0"
    codingFiles = "1"
    creditCards = "2"
    databaseFiles = "4"
    documents = "8"
    mediaFiles = "16"
    unknownFutureValue = "32"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationDataType"
