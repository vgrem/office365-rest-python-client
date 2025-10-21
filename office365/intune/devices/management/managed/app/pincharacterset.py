from enum import Enum


class ManagedAppPinCharacterSet(Enum):
    numeric = "0"
    alphanumericAndSymbol = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedAppPinCharacterSet"
