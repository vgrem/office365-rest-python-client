from enum import Enum


class FailureStage(Enum):
    unknown = "0"
    callSetup = "1"
    midcall = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.callRecords.FailureStage"
