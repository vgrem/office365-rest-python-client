from enum import Enum


class PhysicalAddressType(Enum):
    unknown = "0"
    home = "1"
    business = "2"
    other = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PhysicalAddressType"
