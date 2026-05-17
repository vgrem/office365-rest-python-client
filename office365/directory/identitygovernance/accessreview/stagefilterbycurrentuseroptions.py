from enum import Enum


class AccessReviewStageFilterByCurrentUserOptions(Enum):
    reviewer = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessReviewStageFilterByCurrentUserOptions"
