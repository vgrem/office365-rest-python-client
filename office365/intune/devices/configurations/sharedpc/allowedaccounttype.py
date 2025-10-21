from enum import Enum


class SharedPCAllowedAccountType(Enum):
    guest = "1"
    domain = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SharedPCAllowedAccountType"
