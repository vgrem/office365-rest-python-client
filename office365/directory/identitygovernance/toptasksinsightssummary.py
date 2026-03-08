from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TopTasksInsightsSummary(ClientValue):
    def __init__(
        self,
        failed_tasks: int | None = None,
        failed_users: int | None = None,
        successful_tasks: int | None = None,
        successful_users: int | None = None,
        task_definition_display_name: str | None = None,
        task_definition_id: str | None = None,
        total_tasks: int | None = None,
        total_users: int | None = None,
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
