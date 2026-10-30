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
from office365.runtime.types.odata_property import odata


class UserProcessingResult(Entity):
    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> Optional[datetime]:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="failedTasksCount")
    @property
    def failed_tasks_count(self) -> Optional[int]:
        """Gets the failedTasksCount property"""
        return self.properties.get("failedTasksCount", None)

    @odata(name="processingStatus")
    @property
    def processing_status(self) -> LifecycleWorkflowProcessingStatus:
        """Gets the processingStatus property"""
        return self.properties.get("processingStatus", LifecycleWorkflowProcessingStatus.queued)

    @odata(name="scheduledDateTime")
    @property
    def scheduled_date_time(self) -> Optional[datetime]:
        """Gets the scheduledDateTime property"""
        return self.properties.get("scheduledDateTime", datetime.min)

    @odata(name="startedDateTime")
    @property
    def started_date_time(self) -> Optional[datetime]:
        """Gets the startedDateTime property"""
        return self.properties.get("startedDateTime", datetime.min)

    @odata(name="totalTasksCount")
    @property
    def total_tasks_count(self) -> Optional[int]:
        """Gets the totalTasksCount property"""
        return self.properties.get("totalTasksCount", None)

    @odata(name="totalUnprocessedTasksCount")
    @property
    def total_unprocessed_tasks_count(self) -> Optional[int]:
        """Gets the totalUnprocessedTasksCount property"""
        return self.properties.get("totalUnprocessedTasksCount", None)

    @odata(name="workflowExecutionType")
    @property
    def workflow_execution_type(self) -> WorkflowExecutionType:
        """Gets the workflowExecutionType property"""
        return self.properties.get("workflowExecutionType", WorkflowExecutionType.scheduled)

    @odata(name="workflowVersion")
    @property
    def workflow_version(self) -> Optional[int]:
        """Gets the workflowVersion property"""
        return self.properties.get("workflowVersion", None)

    @odata(name="reprocessedRuns", navigation=True)
    @property
    def reprocessed_runs(self) -> EntityCollection[Run]:
        """Gets the reprocessedRuns property"""
        return self.properties.get(
            "reprocessedRuns",
            EntityCollection[Run](self.context, Run, ResourcePath("reprocessedRuns", self.resource_path)),
        )

    @odata(name="subject", navigation=True)
    @property
    def subject(self) -> User:
        """Gets the subject property"""
        return self.properties.get("subject", User(self.context, ResourcePath("subject", self.resource_path)))

    @odata(name="taskProcessingResults", navigation=True)
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
