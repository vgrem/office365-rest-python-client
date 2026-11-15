from enum import Enum


class PrintJobStateDetail(Enum):
    uploadPending = "0"
    transforming = "1"
    completedSuccessfully = "2"
    completedWithWarnings = "3"
    completedWithErrors = "4"
    releaseWait = "5"
    interpreting = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintJobStateDetail"
