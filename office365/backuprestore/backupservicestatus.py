from enum import Enum


class BackupServiceStatus(Enum):
    disabled = "0"
    enabled = "1"
    protectionChangeLocked = "2"
    restoreLocked = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BackupServiceStatus"
