from enum import Enum


class AndroidWorkProfileRequiredPasswordType(Enum):
    deviceDefault = "0"
    lowSecurityBiometric = "1"
    required = "2"
    atLeastNumeric = "3"
    numericComplex = "4"
    atLeastAlphabetic = "5"
    atLeastAlphanumeric = "6"
    alphanumericWithSymbols = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AndroidWorkProfileRequiredPasswordType"
