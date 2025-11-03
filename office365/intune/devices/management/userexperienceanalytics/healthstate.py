from enum import Enum


class UserExperienceAnalyticsHealthState(Enum):
    unknown = "0"
    insufficientData = "1"
    needsAttention = "2"
    meetingGoals = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserExperienceAnalyticsHealthState"
