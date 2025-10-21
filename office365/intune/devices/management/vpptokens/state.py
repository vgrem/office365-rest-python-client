from enum import Enum


class VppTokenState(Enum):
    unknown = "0"
    valid = "1"
    expired = "2"
    invalid = "3"
    assignedToExternalMDM = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VppTokenState"
