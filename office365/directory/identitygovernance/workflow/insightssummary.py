from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WorkflowsInsightsSummary(ClientValue):
    def __init__(
        self,
        failed_runs: int | None = None,
        failed_tasks: int | None = None,
        failed_users: int | None = None,
        successful_runs: int | None = None,
        successful_tasks: int | None = None,
        successful_users: int | None = None,
        total_runs: int | None = None,
        total_tasks: int | None = None,
        total_users: int | None = None,
    ):
        self.failedRuns = failed_runs
        self.failedTasks = failed_tasks
        self.failedUsers = failed_users
        self.successfulRuns = successful_runs
        self.successfulTasks = successful_tasks
        self.successfulUsers = successful_users
        self.totalRuns = total_runs
        self.totalTasks = total_tasks
        self.totalUsers = total_users

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.WorkflowsInsightsSummary"
