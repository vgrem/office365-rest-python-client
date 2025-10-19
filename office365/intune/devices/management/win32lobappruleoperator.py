from enum import Enum


class Win32LobAppRuleOperator(Enum):
    notConfigured = "0"
    equal = "1"
    notEqual = "2"
    greaterThan = "4"
    greaterThanOrEqual = "5"
    lessThan = "8"
    lessThanOrEqual = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppRuleOperator"
