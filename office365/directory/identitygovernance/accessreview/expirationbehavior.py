from enum import Enum


class AccessReviewExpirationBehavior(Enum):
    keepAccess = "0"
    removeAccess = "1"
    acceptAccessRecommendation = "2"
    unknownFutureValue = "99"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessReviewExpirationBehavior"
