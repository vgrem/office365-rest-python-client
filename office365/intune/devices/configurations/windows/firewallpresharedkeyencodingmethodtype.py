from enum import Enum


class FirewallPreSharedKeyEncodingMethodType(Enum):
    deviceDefault = "0"
    none = "1"
    utF8 = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FirewallPreSharedKeyEncodingMethodType"
