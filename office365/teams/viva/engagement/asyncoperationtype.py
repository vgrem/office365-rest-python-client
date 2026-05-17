from enum import Enum


class EngagementAsyncOperationType(Enum):
    createCommunity = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EngagementAsyncOperationType"
