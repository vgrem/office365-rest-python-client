from enum import Enum


class SendDtmfCompletionReason(Enum):
    unknown = "0"
    completedSuccessfully = "1"
    mediaOperationCanceled = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SendDtmfCompletionReason"
