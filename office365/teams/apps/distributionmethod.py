from enum import Enum


class TeamsAppDistributionMethod(Enum):
    store = "0"
    organization = "1"
    sideloaded = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamsAppDistributionMethod"
