from enum import Enum


class ValueType(Enum):
    enum = "0"
    string = "1"
    int = "2"
    bool = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.ValueType"
