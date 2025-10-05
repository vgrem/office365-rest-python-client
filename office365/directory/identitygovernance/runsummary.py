from office365.runtime.client_value import ClientValue


class RunSummary(ClientValue):

    def __init__(
        self,
        failed_runs: int = None,
        failed_tasks: int = None,
        successful_runs: int = None,
        total_runs: int = None,
        total_tasks: int = None,
        total_users: int = None,
    ):
        self.failedRuns = failed_runs
        self.failedTasks = failed_tasks
        self.successfulRuns = successful_runs
        self.totalRuns = total_runs
        self.totalTasks = total_tasks
        self.totalUsers = total_users
