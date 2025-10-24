from enum import Enum


class PlannerContainerType(Enum):
    group = "1"
    unknownFutureValue = "2"
    roster = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PlannerContainerType"
