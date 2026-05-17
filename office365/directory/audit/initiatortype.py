from enum import Enum


class InitiatorType(Enum):
    user = "0"
    application = "1"
    system = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.InitiatorType"
