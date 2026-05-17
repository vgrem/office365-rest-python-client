from enum import Enum


class RequiredPasswordType(Enum):
    deviceDefault = "0"
    alphanumeric = "1"
    numeric = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RequiredPasswordType"
