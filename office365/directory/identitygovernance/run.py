from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.identitygovernance.activationscope import ActivationScope
from office365.directory.identitygovernance.lifecycleworkflowprocessingstatus import (
    LifecycleWorkflowProcessingStatus,
)
from office365.directory.identitygovernance.task_processing_result import (
    TaskProcessingResult,
)
from office365.directory.identitygovernance.workflow.executiontype import (
    WorkflowExecutionType,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.subject_processing_result import (
        SubjectProcessingResult,
    )
    from office365.directory.identitygovernance.user_processing_result import (
        UserProcessingResult,
    )


class Run(Entity):
    @odata(name="activatedOnScope")
    @property
    def activated_on_scope(self) -> ActivationScope:
        """Gets the activatedOnScope property"""
        return self.properties.get("activatedOnScope", ActivationScope())

    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> datetime:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="failedTasksCount")
    @property
    def failed_tasks_count(self) -> Optional[int]:
        """Gets the failedTasksCount property"""
        return self.properties.get("failedTasksCount", None)

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

    @odata(name="scheduledDateTime")
    @property
    def scheduled_date_time(self) -> datetime:
        """Gets the scheduledDateTime property"""
        return self.properties.get("scheduledDateTime", datetime.min)

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

    @odata(name="totalUsersCount")
    @property
    def total_users_count(self) -> Optional[int]:
        """Gets the totalUsersCount property"""
        return self.properties.get("totalUsersCount", None)

    @odata(name="workflowExecutionType")
    @property
    def workflow_execution_type(self) -> WorkflowExecutionType:
        """Gets the workflowExecutionType property"""
        return self.properties.get("workflowExecutionType", WorkflowExecutionType.scheduled)

    @odata(name="reprocessedRuns", navigation=True)
    @property
    def reprocessed_runs(self) -> EntityCollection[Run]:
        """Gets the reprocessedRuns property"""
        return self.properties.get(
            "reprocessedRuns",
            EntityCollection[Run](self.context, Run, ResourcePath("reprocessedRuns", self.resource_path)),
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

    @odata(name="userProcessingResults", navigation=True)
    @property
    def user_processing_results(self) -> EntityCollection[UserProcessingResult]:
        """Gets the userProcessingResults property"""
        from office365.directory.identitygovernance.user_processing_result import (
            UserProcessingResult,
        )

        return self.properties.get(
            "userProcessingResults",
            EntityCollection[UserProcessingResult](
                self.context, UserProcessingResult, ResourcePath("userProcessingResults", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.Run"

    @odata(name="subjectProcessingResults", navigation=True)
    @property
    def subject_processing_results(self) -> EntityCollection[SubjectProcessingResult]:
        """Gets the subjectProcessingResults property"""
        from office365.directory.identitygovernance.subject_processing_result import (
            SubjectProcessingResult,
        )

        return self.properties.get(
            "subjectProcessingResults",
            EntityCollection[SubjectProcessingResult](
                self.context, SubjectProcessingResult, ResourcePath("subjectProcessingResults", self.resource_path)
            ),
        )
