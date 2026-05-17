from enum import Enum


class AccessReviewHistoryStatus(Enum):
    done = "0"
    inprogress = "1"
    error = "2"
    requested = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessReviewHistoryStatus"
