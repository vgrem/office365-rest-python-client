from enum import Enum


class ManagedAppAvailability(Enum):
    global_ = "0"
    lineOfBusiness = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedAppAvailability"
