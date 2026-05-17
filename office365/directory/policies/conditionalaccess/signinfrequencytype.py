from enum import Enum


class SigninFrequencyType(Enum):
    days = "0"
    hours = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SigninFrequencyType"
