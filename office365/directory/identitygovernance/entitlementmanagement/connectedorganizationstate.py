from enum import Enum


class ConnectedOrganizationState(Enum):
    configured = "0"
    proposed = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConnectedOrganizationState"
