from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.directory.identitygovernance.toptasksinsightssummary import TopTasksInsightsSummary
    from office365.directory.identitygovernance.topworkflowsinsightssummary import TopWorkflowsInsightsSummary
    from office365.directory.identitygovernance.workflow.insightsbycategory import WorkflowsInsightsByCategory
    from office365.directory.identitygovernance.workflow.insightssummary import WorkflowsInsightsSummary


class Insights(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.Insights"

    @verb(role="action", effect="read")
    @require_permission(
        delegated=["LifecycleWorkflows.Read.All", "LifecycleWorkflows.ReadWrite.All"],
        application=["LifecycleWorkflows.Read.All", "LifecycleWorkflows.ReadWrite.All"],
    )
    def top_tasks_processed_summary(
        self, start_date_time: datetime, end_date_time: datetime
    ) -> ClientResult[ClientValueCollection[TopTasksInsightsSummary]]:
        """topTasksProcessedSummary operation.

        Args:
            start_date_time (datetime):
                startDateTime parameter
            end_date_time (datetime):
                endDateTime parameter
        """
        from office365.directory.identitygovernance.toptasksinsightssummary import TopTasksInsightsSummary

        return_type = ClientResult(self.context, ClientValueCollection(TopTasksInsightsSummary))
        qry = FunctionQuery(
            self,
            "topTasksProcessedSummary",
            {"startDateTime": start_date_time, "endDateTime": end_date_time},
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="read")
    @require_permission(
        delegated=["LifecycleWorkflows.Read.All", "LifecycleWorkflows.ReadWrite.All"],
        application=["LifecycleWorkflows.Read.All", "LifecycleWorkflows.ReadWrite.All"],
    )
    def top_workflows_processed_summary(
        self, start_date_time: datetime, end_date_time: datetime
    ) -> ClientResult[ClientValueCollection[TopWorkflowsInsightsSummary]]:
        """topWorkflowsProcessedSummary operation.

        Args:
            start_date_time (datetime):
                startDateTime parameter
            end_date_time (datetime):
                endDateTime parameter
        """
        from office365.directory.identitygovernance.topworkflowsinsightssummary import TopWorkflowsInsightsSummary

        return_type = ClientResult(self.context, ClientValueCollection(TopWorkflowsInsightsSummary))
        qry = FunctionQuery(
            self,
            "topWorkflowsProcessedSummary",
            {"startDateTime": start_date_time, "endDateTime": end_date_time},
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="read")
    @require_permission(
        delegated=["LifecycleWorkflows.Read.All", "LifecycleWorkflows.ReadWrite.All"],
        application=["LifecycleWorkflows.Read.All", "LifecycleWorkflows.ReadWrite.All"],
    )
    def workflows_processed_by_category(
        self, start_date_time: datetime, end_date_time: datetime
    ) -> ClientResult[WorkflowsInsightsByCategory]:
        """workflowsProcessedByCategory operation.

        Args:
            start_date_time (datetime):
                startDateTime parameter
            end_date_time (datetime):
                endDateTime parameter
        """
        from office365.directory.identitygovernance.workflow.insightsbycategory import WorkflowsInsightsByCategory

        return_type = ClientResult(self.context, WorkflowsInsightsByCategory())
        qry = FunctionQuery(
            self,
            "workflowsProcessedByCategory",
            {"startDateTime": start_date_time, "endDateTime": end_date_time},
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="read")
    @require_permission(
        delegated=["LifecycleWorkflows.Read.All", "LifecycleWorkflows.ReadWrite.All"],
        application=["LifecycleWorkflows.Read.All", "LifecycleWorkflows.ReadWrite.All"],
    )
    def workflows_processed_summary(
        self, start_date_time: datetime, end_date_time: datetime
    ) -> ClientResult[WorkflowsInsightsSummary]:
        """workflowsProcessedSummary operation.

        Args:
            start_date_time (datetime):
                startDateTime parameter
            end_date_time (datetime):
                endDateTime parameter
        """
        from office365.directory.identitygovernance.workflow.insightssummary import WorkflowsInsightsSummary

        return_type = ClientResult(self.context, WorkflowsInsightsSummary())
        qry = FunctionQuery(
            self,
            "workflowsProcessedSummary",
            {"startDateTime": start_date_time, "endDateTime": end_date_time},
            return_type,
        )
        self.context.add_query(qry)
        return return_type
