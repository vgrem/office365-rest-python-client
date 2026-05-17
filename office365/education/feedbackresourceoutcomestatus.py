from enum import Enum


class EducationFeedbackResourceOutcomeStatus(Enum):
    notPublished = "0"
    pendingPublish = "1"
    published = "2"
    failedPublish = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationFeedbackResourceOutcomeStatus"
