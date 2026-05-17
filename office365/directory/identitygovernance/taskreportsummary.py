from typing import Optional

from office365.runtime.client_value import ClientValue


class TaskReportSummary(ClientValue):
    def __init__(
        self,
        failed_tasks: Optional[int] = None,
        successful_tasks: Optional[int] = None,
        total_tasks: Optional[int] = None,
        unprocessed_tasks: Optional[int] = None,
    ):
        self.failedTasks = failed_tasks
        self.successfulTasks = successful_tasks
        self.totalTasks = total_tasks
        self.unprocessedTasks = unprocessed_tasks

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TaskReportSummary"
