from enum import Enum


class UserExperienceAnalyticsInsightSeverity(Enum):
    none = "0"
    informational = "1"
    warning = "2"
    error = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserExperienceAnalyticsInsightSeverity"
