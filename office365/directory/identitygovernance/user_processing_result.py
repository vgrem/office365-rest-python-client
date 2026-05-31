from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.lifecycleworkflowprocessingstatus import LifecycleWorkflowProcessingStatus
from office365.directory.identitygovernance.run import Run
from office365.directory.identitygovernance.task_processing_result import TaskProcessingResult
from office365.directory.identitygovernance.workflow.executiontype import WorkflowExecutionType
from office365.directory.users.user import User
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class UserProcessingResult(Entity):
    @property
    def completed_date_time(self) -> datetime:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @property
    def failed_tasks_count(self) -> Optional[int]:
        """Gets the failedTasksCount property"""
        return self.properties.get("failedTasksCount", None)

    @property
    def processing_status(self) -> LifecycleWorkflowProcessingStatus:
        """Gets the processingStatus property"""
        return self.properties.get("processingStatus", LifecycleWorkflowProcessingStatus.queued)

    @property
    def scheduled_date_time(self) -> datetime:
        """Gets the scheduledDateTime property"""
        return self.properties.get("scheduledDateTime", datetime.min)

    @property
    def started_date_time(self) -> datetime:
        """Gets the startedDateTime property"""
        return self.properties.get("startedDateTime", datetime.min)

    @property
    def total_tasks_count(self) -> Optional[int]:
        """Gets the totalTasksCount property"""
        return self.properties.get("totalTasksCount", None)

    @property
    def total_unprocessed_tasks_count(self) -> Optional[int]:
        """Gets the totalUnprocessedTasksCount property"""
        return self.properties.get("totalUnprocessedTasksCount", None)

    @property
    def workflow_execution_type(self) -> WorkflowExecutionType:
        """Gets the workflowExecutionType property"""
        return self.properties.get("workflowExecutionType", WorkflowExecutionType.scheduled)

    @property
    def workflow_version(self) -> Optional[int]:
        """Gets the workflowVersion property"""
        return self.properties.get("workflowVersion", None)

    @property
    def reprocessed_runs(self) -> EntityCollection[Run]:
        """Gets the reprocessedRuns property"""
        return self.properties.get(
            "reprocessedRuns",
            EntityCollection[Run](self.context, Run, ResourcePath("reprocessedRuns", self.resource_path)),
        )

    @property
    def subject(self) -> User:
        """Gets the subject property"""
        return self.properties.get("subject", User(self.context, ResourcePath("subject", self.resource_path)))

    @property
    def task_processing_results(self) -> EntityCollection[TaskProcessingResult]:
        """Gets the taskProcessingResults property"""
        return self.properties.get(
            "taskProcessingResults",
            EntityCollection[TaskProcessingResult](
                self.context, TaskProcessingResult, ResourcePath("taskProcessingResults", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.UserProcessingResult"
