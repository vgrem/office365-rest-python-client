from enum import Enum


class UserSignInRecommendationScope(Enum):
    tenant = "0"
    application = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserSignInRecommendationScope"
