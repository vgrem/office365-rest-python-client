from enum import Enum


class BitLockerEncryptionMethod(Enum):
    aesCbc128 = "3"
    aesCbc256 = "4"
    xtsAes128 = "6"
    xtsAes256 = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BitLockerEncryptionMethod"
