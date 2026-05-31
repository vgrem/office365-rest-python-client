from enum import Enum


class AuthenticationAttributeCollectionInputType(Enum):
    text = "1"
    radioSingleSelect = "2"
    checkboxMultiSelect = "3"
    boolean = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationAttributeCollectionInputType"
