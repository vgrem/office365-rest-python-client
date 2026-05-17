from enum import Enum


class ObjectFlowTypes(Enum):
    None_ = "0"
    Add = "1"
    Update = "2"
    Delete = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ObjectFlowTypes"
