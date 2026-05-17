from enum import Enum


class AndroidRequiredPasswordType(Enum):
    deviceDefault = "0"
    alphabetic = "1"
    alphanumeric = "2"
    alphanumericWithSymbols = "3"
    lowSecurityBiometric = "4"
    numeric = "5"
    numericComplex = "6"
    any = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AndroidRequiredPasswordType"
