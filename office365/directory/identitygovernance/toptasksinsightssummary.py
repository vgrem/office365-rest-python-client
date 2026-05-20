from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TopTasksInsightsSummary(ClientValue):
    failedTasks: int | None = None
    failedUsers: int | None = None
    successfulTasks: int | None = None
    successfulUsers: int | None = None
    taskDefinitionDisplayName: str | None = None
    taskDefinitionId: str | None = None
    totalTasks: int | None = None
    totalUsers: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TopTasksInsightsSummary"
