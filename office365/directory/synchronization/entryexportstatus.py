from enum import Enum


class EntryExportStatus(Enum):
    Noop = "0"
    Success = "1"
    RetryableError = "2"
    PermanentError = "3"
    Error = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EntryExportStatus"
