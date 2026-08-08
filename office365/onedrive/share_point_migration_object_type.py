from __future__ import annotations

from enum import Enum


class SharePointMigrationObjectType(Enum):
    site = "0"
    web = "1"
    folder = "2"
    list = "3"
    listItem = "4"
    file = "5"
    alert = "6"
    sharedWithObject = "7"
    invalid = "8"
    unknownFutureValue = "9"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationObjectType"
