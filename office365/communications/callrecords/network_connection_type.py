from __future__ import annotations

from enum import Enum


class NetworkConnectionType(Enum):
    unknown = "0"
    wired = "1"
    wifi = "2"
    mobile = "3"
    tunnel = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.NetworkConnectionType"
