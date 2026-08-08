from __future__ import annotations

from enum import Enum


class NetworkTransportProtocol(Enum):
    unknown = "0"
    udp = "1"
    tcp = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.NetworkTransportProtocol"
