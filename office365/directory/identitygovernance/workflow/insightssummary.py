from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WorkflowsInsightsSummary(ClientValue):
    failedRuns: int | None = None
    failedTasks: int | None = None
    failedUsers: int | None = None
    successfulRuns: int | None = None
    successfulTasks: int | None = None
    successfulUsers: int | None = None
    totalRuns: int | None = None
    totalTasks: int | None = None
    totalUsers: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.WorkflowsInsightsSummary"
