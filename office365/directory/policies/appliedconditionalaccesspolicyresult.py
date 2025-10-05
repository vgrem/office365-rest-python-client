from enum import Enum


class AppliedConditionalAccessPolicyResult(Enum):
    success = "0"
    failure = "1"
    notApplied = "2"
    notEnabled = "3"
    unknown = "4"
    unknownFutureValue = "5"
    reportOnlySuccess = "6"
    reportOnlyFailure = "7"
    reportOnlyNotApplied = "8"
    reportOnlyInterrupted = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppliedConditionalAccessPolicyResult"
