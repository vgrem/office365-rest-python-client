from enum import Enum


class BackupServiceConsumer(Enum):
    unknown = "0"
    firstparty = "1"
    thirdparty = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BackupServiceConsumer"
