from office365.runtime.client_value import ClientValue


class WorkflowsInsightsByCategory(ClientValue):
    def __init__(
        self,
        failed_joiner_runs: int = None,
        failed_leaver_runs: int = None,
        failed_mover_runs: int = None,
        successful_joiner_runs: int = None,
        successful_leaver_runs: int = None,
        successful_mover_runs: int = None,
        total_joiner_runs: int = None,
        total_leaver_runs: int = None,
        total_mover_runs: int = None,
    ):
        self.failedJoinerRuns = failed_joiner_runs
        self.failedLeaverRuns = failed_leaver_runs
        self.failedMoverRuns = failed_mover_runs
        self.successfulJoinerRuns = successful_joiner_runs
        self.successfulLeaverRuns = successful_leaver_runs
        self.successfulMoverRuns = successful_mover_runs
        self.totalJoinerRuns = total_joiner_runs
        self.totalLeaverRuns = total_leaver_runs
        self.totalMoverRuns = total_mover_runs

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.WorkflowsInsightsByCategory"
