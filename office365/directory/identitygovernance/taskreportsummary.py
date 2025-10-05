from office365.runtime.client_value import ClientValue


class TaskReportSummary(ClientValue):

    def __init__(
        self,
        failed_tasks: int = None,
        successful_tasks: int = None,
        total_tasks: int = None,
        unprocessed_tasks: int = None,
    ):
        self.failedTasks = failed_tasks
        self.successfulTasks = successful_tasks
        self.totalTasks = total_tasks
        self.unprocessedTasks = unprocessed_tasks
