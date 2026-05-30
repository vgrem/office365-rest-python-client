from __future__ import annotations

from enum import Enum


class SslVersion(Enum):
    none = "0"
    ssl3_0 = "1"
    tls1_0 = "2"
    tls1_1 = "3"
    tls1_2 = "4"
    tls1_3 = "5"
    notSupported = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SslVersion"
