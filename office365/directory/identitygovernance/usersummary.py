from office365.runtime.client_value import ClientValue


class UserSummary(ClientValue):
    def __init__(
        self,
        failed_tasks: int = None,
        failed_users: int = None,
        successful_users: int = None,
        total_tasks: int = None,
        total_users: int = None,
    ):
        self.failedTasks = failed_tasks
        self.failedUsers = failed_users
        self.successfulUsers = successful_users
        self.totalTasks = total_tasks
        self.totalUsers = total_users

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.UserSummary"
