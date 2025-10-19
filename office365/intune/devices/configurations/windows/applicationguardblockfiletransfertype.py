from enum import Enum


class ApplicationGuardBlockFileTransferType(Enum):
    notConfigured = "0"
    blockImageAndTextFile = "1"
    blockImageFile = "2"
    blockNone = "3"
    blockTextFile = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ApplicationGuardBlockFileTransferType"
