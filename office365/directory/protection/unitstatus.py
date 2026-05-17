from enum import Enum


class ProtectionUnitStatus(Enum):
    protectRequested = "0"
    protected = "1"
    unprotectRequested = "2"
    unprotected = "3"
    removeRequested = "4"
    unknownFutureValue = "5"
    offboardRequested = "6"
    offboarded = "7"
    cancelOffboardRequested = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProtectionUnitStatus"
