from enum import Enum


class Win32LobAppPowerShellScriptRuleOperationType(Enum):
    notConfigured = "0"
    string = "1"
    dateTime = "2"
    integer = "3"
    float = "4"
    version = "5"
    boolean = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppPowerShellScriptRuleOperationType"
