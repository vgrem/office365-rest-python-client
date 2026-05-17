from enum import Enum


class RunAsAccountType(Enum):
    system = "0"
    user = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RunAsAccountType"
