from enum import Enum


class Mutability(Enum):
    ReadWrite = "0"
    ReadOnly = "1"
    Immutable = "2"
    WriteOnly = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Mutability"
