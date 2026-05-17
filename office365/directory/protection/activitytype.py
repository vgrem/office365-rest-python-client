from enum import Enum


class ActivityType(Enum):
    signin = "0"
    user = "1"
    unknownFutureValue = "2"
    servicePrincipal = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ActivityType"
