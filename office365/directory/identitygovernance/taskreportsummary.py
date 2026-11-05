from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TaskReportSummary(ClientValue):
    failedTasks: int | None = None
    successfulTasks: int | None = None
    totalTasks: int | None = None
    unprocessedTasks: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TaskReportSummary"
