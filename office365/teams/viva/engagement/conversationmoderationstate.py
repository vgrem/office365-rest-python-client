from enum import Enum


class EngagementConversationModerationState(Enum):
    published = "0"
    pendingReview = "1"
    dismissed = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EngagementConversationModerationState"
