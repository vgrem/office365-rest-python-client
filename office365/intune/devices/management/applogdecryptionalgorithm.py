from enum import Enum


class AppLogDecryptionAlgorithm(Enum):
    aes256 = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppLogDecryptionAlgorithm"
