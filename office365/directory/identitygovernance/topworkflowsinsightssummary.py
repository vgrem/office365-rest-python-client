from office365.directory.identitygovernance.workflow.lifecycleworkflowcategory import (
    LifecycleWorkflowCategory,
)
from office365.runtime.client_value import ClientValue


class TopWorkflowsInsightsSummary(ClientValue):

    def __init__(
        self,
        failed_runs: int = None,
        failed_users: int = None,
        successful_runs: int = None,
        successful_users: int = None,
        total_runs: int = None,
        total_users: int = None,
        workflow_category: LifecycleWorkflowCategory = None,
        workflow_display_name: str = None,
        workflow_id: str = None,
        workflow_version: int = None,
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
