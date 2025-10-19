from enum import Enum


class Win32LobAppRuleType(Enum):
    detection = "0"
    requirement = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppRuleType"
