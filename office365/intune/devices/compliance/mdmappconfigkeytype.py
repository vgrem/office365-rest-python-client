from enum import Enum


class MdmAppConfigKeyType(Enum):
    stringType = "0"
    integerType = "1"
    realType = "2"
    booleanType = "3"
    tokenType = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MdmAppConfigKeyType"
