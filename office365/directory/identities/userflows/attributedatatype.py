from enum import Enum


class IdentityUserFlowAttributeDataType(Enum):
    string = "1"
    boolean = "2"
    int64 = "3"
    stringCollection = "4"
    dateTime = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.IdentityUserFlowAttributeDataType"
