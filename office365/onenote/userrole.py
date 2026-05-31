from enum import Enum


class OnenoteUserRole(Enum):
    Unknown = "-1"
    Owner = "0"
    Contributor = "1"
    Reader = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnenoteUserRole"
