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
from office365.runtime.types.odata_property import odata


class TaskReport(Entity):
    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> datetime:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="failedUsersCount")
    @property
    def failed_users_count(self) -> Optional[int]:
        """Gets the failedUsersCount property"""
        return self.properties.get("failedUsersCount", None)

    @odata(name="lastUpdatedDateTime")
    @property
    def last_updated_date_time(self) -> datetime:
        """Gets the lastUpdatedDateTime property"""
        return self.properties.get("lastUpdatedDateTime", datetime.min)

    @odata(name="processingStatus")
    @property
    def processing_status(self) -> LifecycleWorkflowProcessingStatus:
        """Gets the processingStatus property"""
        return self.properties.get("processingStatus", LifecycleWorkflowProcessingStatus.queued)

    @odata(name="runId")
    @property
    def run_id(self) -> Optional[str]:
        """Gets the runId property"""
        return self.properties.get("runId", None)

    @odata(name="startedDateTime")
    @property
    def started_date_time(self) -> datetime:
        """Gets the startedDateTime property"""
        return self.properties.get("startedDateTime", datetime.min)

    @odata(name="successfulUsersCount")
    @property
    def successful_users_count(self) -> Optional[int]:
        """Gets the successfulUsersCount property"""
        return self.properties.get("successfulUsersCount", None)

    @odata(name="totalUsersCount")
    @property
    def total_users_count(self) -> Optional[int]:
        """Gets the totalUsersCount property"""
        return self.properties.get("totalUsersCount", None)

    @odata(name="unprocessedUsersCount")
    @property
    def unprocessed_users_count(self) -> Optional[int]:
        """Gets the unprocessedUsersCount property"""
        return self.properties.get("unprocessedUsersCount", None)

    @odata(name="task", navigation=True)
    @property
    def task(self) -> Task:
        """Gets the task property"""
        return self.properties.get("task", Task(self.context, ResourcePath("task", self.resource_path)))

    @odata(name="taskDefinition", navigation=True)
    @property
    def task_definition(self) -> TaskDefinition:
        """Gets the taskDefinition property"""
        return self.properties.get(
            "taskDefinition", TaskDefinition(self.context, ResourcePath("taskDefinition", self.resource_path))
        )

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
        return "microsoft.graph.identityGovernance.TaskReport"
