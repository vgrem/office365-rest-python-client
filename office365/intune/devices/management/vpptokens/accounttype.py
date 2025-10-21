from enum import Enum


class VppTokenAccountType(Enum):
    business = "0"
    education = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VppTokenAccountType"
