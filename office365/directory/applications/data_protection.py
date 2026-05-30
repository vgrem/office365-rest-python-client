from __future__ import annotations

from enum import Enum


class DataProtection(Enum):
    none = "0"
    impactAssessments = "1"
    officers = "2"
    secureCrossBorderDataTransfer = "4"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DataProtection"
