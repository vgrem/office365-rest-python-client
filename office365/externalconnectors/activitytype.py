from enum import Enum


class ExternalActivityType(Enum):
    viewed = "1"
    modified = "2"
    created = "3"
    commented = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.externalConnectors.ExternalActivityType"
