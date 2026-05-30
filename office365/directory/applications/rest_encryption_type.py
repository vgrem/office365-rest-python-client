from __future__ import annotations

from enum import Enum


class RestEncryptionType(Enum):
    none = "0"
    aes = "1"
    bitlocker = "2"
    blowfish = "3"
    des = "4"
    rc4 = "5"
    rsa = "6"
    notSupported = "7"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestEncryptionType"
