from __future__ import annotations

from enum import Enum


class PciVersion(Enum):
    none = "0"
    v3_2_1 = "1"
    v4 = "2"
    notSupported = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PciVersion"
