from enum import Enum


class AppLogUploadState(Enum):
    pending = "0"
    completed = "1"
    failed = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppLogUploadState"
