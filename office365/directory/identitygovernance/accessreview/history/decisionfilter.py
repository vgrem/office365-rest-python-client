from enum import Enum


class AccessReviewHistoryDecisionFilter(Enum):
    approve = "0"
    deny = "1"
    notReviewed = "2"
    dontKnow = "3"
    notNotified = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessReviewHistoryDecisionFilter"
