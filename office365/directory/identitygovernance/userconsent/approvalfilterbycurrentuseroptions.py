from enum import Enum


class ApprovalFilterByCurrentUserOptions(Enum):
    target = "0"
    createdBy = "1"
    approver = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ApprovalFilterByCurrentUserOptions"
