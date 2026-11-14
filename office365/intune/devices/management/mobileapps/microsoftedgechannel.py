from enum import Enum


class MicrosoftEdgeChannel(Enum):
    dev = "0"
    beta = "1"
    stable = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MicrosoftEdgeChannel"
