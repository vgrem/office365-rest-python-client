from office365.runtime.client_value import ClientValue


class TopTasksInsightsSummary(ClientValue):
    def __init__(
        self,
        failed_tasks: int = None,
        failed_users: int = None,
        successful_tasks: int = None,
        successful_users: int = None,
        task_definition_display_name: str = None,
        task_definition_id: str = None,
        total_tasks: int = None,
        total_users: int = None,
    ):
        self.failedTasks = failed_tasks
        self.failedUsers = failed_users
        self.successfulTasks = successful_tasks
        self.successfulUsers = successful_users
        self.taskDefinitionDisplayName = task_definition_display_name
        self.taskDefinitionId = task_definition_id
        self.totalTasks = total_tasks
        self.totalUsers = total_users

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TopTasksInsightsSummary"
