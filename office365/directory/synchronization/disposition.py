from enum import Enum


class SynchronizationDisposition(Enum):
    Normal = "0"
    Discard = "1"
    Escrow = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SynchronizationDisposition"
