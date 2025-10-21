from enum import Enum


class ActionState(Enum):
    none = "0"
    pending = "1"
    canceled = "2"
    active = "3"
    done = "4"
    failed = "5"
    notSupported = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ActionState"
