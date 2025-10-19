from enum import Enum


class EntrySyncOperation(Enum):
    None_ = "0"
    Add = "1"
    Delete = "2"
    Update = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EntrySyncOperation"
