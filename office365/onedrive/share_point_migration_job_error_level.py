from __future__ import annotations

from enum import Enum


class SharePointMigrationJobErrorLevel(Enum):
    important = "0"
    warning = "1"
    error = "2"
    fatalError = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobErrorLevel"
