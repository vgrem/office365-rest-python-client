from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WorkflowsInsightsByCategory(ClientValue):
    failedJoinerRuns: int | None = None
    failedLeaverRuns: int | None = None
    failedMoverRuns: int | None = None
    successfulJoinerRuns: int | None = None
    successfulLeaverRuns: int | None = None
    successfulMoverRuns: int | None = None
    totalJoinerRuns: int | None = None
    totalLeaverRuns: int | None = None
    totalMoverRuns: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.WorkflowsInsightsByCategory"
