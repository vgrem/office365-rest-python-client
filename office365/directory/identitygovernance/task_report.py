from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.lifecycleworkflowprocessingstatus import LifecycleWorkflowProcessingStatus
from office365.directory.identitygovernance.task import Task
from office365.directory.identitygovernance.task_definition import TaskDefinition
from office365.directory.identitygovernance.task_processing_result import TaskProcessingResult
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class TaskReport(Entity):
    @property
    def completed_date_time(self) -> datetime:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @property
    def failed_users_count(self) -> Optional[int]:
        """Gets the failedUsersCount property"""
        return self.properties.get("failedUsersCount", None)

    @property
    def last_updated_date_time(self) -> datetime:
        """Gets the lastUpdatedDateTime property"""
        return self.properties.get("lastUpdatedDateTime", datetime.min)

    @property
    def processing_status(self) -> LifecycleWorkflowProcessingStatus:
        """Gets the processingStatus property"""
        return self.properties.get("processingStatus", LifecycleWorkflowProcessingStatus.queued)

    @property
    def run_id(self) -> Optional[str]:
        """Gets the runId property"""
        return self.properties.get("runId", None)

    @property
    def started_date_time(self) -> datetime:
        """Gets the startedDateTime property"""
        return self.properties.get("startedDateTime", datetime.min)

    @property
    def successful_users_count(self) -> Optional[int]:
        """Gets the successfulUsersCount property"""
        return self.properties.get("successfulUsersCount", None)

    @property
    def total_users_count(self) -> Optional[int]:
        """Gets the totalUsersCount property"""
        return self.properties.get("totalUsersCount", None)

    @property
    def unprocessed_users_count(self) -> Optional[int]:
        """Gets the unprocessedUsersCount property"""
        return self.properties.get("unprocessedUsersCount", None)

    @property
    def task(self) -> Task:
        """Gets the task property"""
        return self.properties.get("task", Task(self.context, ResourcePath("task", self.resource_path)))

    @property
    def task_definition(self) -> TaskDefinition:
        """Gets the taskDefinition property"""
        return self.properties.get(
            "taskDefinition", TaskDefinition(self.context, ResourcePath("taskDefinition", self.resource_path))
        )

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
        return "microsoft.graph.identityGovernance.TaskReport"
