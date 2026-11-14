from __future__ import annotations

from enum import Enum


class RoleAssignmentScheduleRequestFilterByCurrentUserOptions(Enum):
    principal = "1"
    createdBy = "2"
    approver = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RoleAssignmentScheduleRequestFilterByCurrentUserOptions"
