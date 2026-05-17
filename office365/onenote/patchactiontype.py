from enum import Enum


class OnenotePatchActionType(Enum):
    Replace = "0"
    Append = "1"
    Delete = "2"
    Insert = "3"
    Prepend = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnenotePatchActionType"
