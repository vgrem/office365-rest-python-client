from __future__ import annotations

from enum import Enum


class FedRampLevel(Enum):
    none = "0"
    high = "1"
    liSaas = "2"
    low = "3"
    moderate = "4"
    notSupported = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FedRampLevel"
