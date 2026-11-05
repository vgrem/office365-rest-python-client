from __future__ import annotations

from office365.runtime.client_value import ClientValue


class RunSummary(ClientValue):
    failedRuns: int | None = None
    failedTasks: int | None = None
    successfulRuns: int | None = None
    totalRuns: int | None = None
    totalTasks: int | None = None
    totalUsers: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.RunSummary"
