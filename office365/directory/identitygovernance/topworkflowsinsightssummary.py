from __future__ import annotations

from office365.directory.identitygovernance.lifecycleworkflows.category import LifecycleWorkflowCategory
from office365.runtime.client_value import ClientValue


class TopWorkflowsInsightsSummary(ClientValue):
    def __init__(
        self,
        failed_runs: int | None = None,
        failed_users: int | None = None,
        successful_runs: int | None = None,
        successful_users: int | None = None,
        total_runs: int | None = None,
        total_users: int | None = None,
        workflow_category: LifecycleWorkflowCategory | None = None,
        workflow_display_name: str | None = None,
        workflow_id: str | None = None,
        workflow_version: int | None = None,
    ):
        self.failedRuns = failed_runs
        self.failedUsers = failed_users
        self.successfulRuns = successful_runs
        self.successfulUsers = successful_users
        self.totalRuns = total_runs
        self.totalUsers = total_users
        self.workflowCategory = workflow_category
        self.workflowDisplayName = workflow_display_name
        self.workflowId = workflow_id
        self.workflowVersion = workflow_version

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TopWorkflowsInsightsSummary"
