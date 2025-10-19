from enum import Enum


class Win32LobAppRegistryRuleOperationType(Enum):
    notConfigured = "0"
    exists = "1"
    doesNotExist = "2"
    string = "3"
    integer = "4"
    version = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppRegistryRuleOperationType"
