from enum import Enum


class OnlineMeetingContentSharingDisabledReason(Enum):
    watermarkProtection = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnlineMeetingContentSharingDisabledReason"
