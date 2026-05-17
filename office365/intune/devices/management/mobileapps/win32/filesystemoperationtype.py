from enum import Enum


class Win32LobAppFileSystemOperationType(Enum):
    notConfigured = "0"
    exists = "1"
    modifiedDate = "2"
    createdDate = "3"
    version = "4"
    sizeInMB = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppFileSystemOperationType"
