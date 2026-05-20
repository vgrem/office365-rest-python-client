from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identitygovernance.lifecycleworkflows.category import LifecycleWorkflowCategory
from office365.runtime.client_value import ClientValue


@dataclass
class TopWorkflowsInsightsSummary(ClientValue):
    failedRuns: int | None = None
    failedUsers: int | None = None
    successfulRuns: int | None = None
    successfulUsers: int | None = None
    totalRuns: int | None = None
    totalUsers: int | None = None
    workflowCategory: LifecycleWorkflowCategory | None = None
    workflowDisplayName: str | None = None
    workflowId: str | None = None
    workflowVersion: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TopWorkflowsInsightsSummary"
