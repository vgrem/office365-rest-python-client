from __future__ import annotations

from enum import Enum


class DataRetentionLevel(Enum):
    none = "0"
    dataRetained = "1"
    deletedImmediately = "2"
    deletedWithin1Month = "3"
    deletedWithin2Weeks = "4"
    deletedWithin3Months = "5"
    deletedWithinMoreThan3Months = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DataRetentionLevel"
