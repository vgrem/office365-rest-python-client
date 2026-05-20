from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
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
