from typing import Optional

from office365.runtime.client_value import ClientValue


class RunSummary(ClientValue):
    def __init__(
        self,
        failed_runs: Optional[int] = None,
        failed_tasks: Optional[int] = None,
        successful_runs: Optional[int] = None,
        total_runs: Optional[int] = None,
        total_tasks: Optional[int] = None,
        total_users: Optional[int] = None,
    ):
        self.failedRuns = failed_runs
        self.failedTasks = failed_tasks
        self.successfulRuns = successful_runs
        self.totalRuns = total_runs
        self.totalTasks = total_tasks
        self.totalUsers = total_users

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.RunSummary"
