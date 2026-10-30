from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.lifecycleworkflowprocessingstatus import (
    LifecycleWorkflowProcessingStatus,
)
from office365.directory.identitygovernance.task import Task
from office365.directory.identitygovernance.workflow.subject import WorkflowSubject
from office365.directory.users.user import User
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class TaskProcessingResult(Entity):
    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> datetime:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="failureReason")
    @property
    def failure_reason(self) -> Optional[str]:
        """Gets the failureReason property"""
        return self.properties.get("failureReason", None)

    @odata(name="processingInfo")
    @property
    def processing_info(self) -> Optional[str]:
        """Gets the processingInfo property"""
        return self.properties.get("processingInfo", None)

    @odata(name="processingStatus")
    @property
    def processing_status(self) -> LifecycleWorkflowProcessingStatus:
        """Gets the processingStatus property"""
        return self.properties.get("processingStatus", LifecycleWorkflowProcessingStatus.queued)

    @odata(name="startedDateTime")
    @property
    def started_date_time(self) -> datetime:
        """Gets the startedDateTime property"""
        return self.properties.get("startedDateTime", datetime.min)

    @odata(name="subject", navigation=True)
    @property
    def subject(self) -> User:
        """Gets the subject property"""
        return self.properties.get("subject", User(self.context, ResourcePath("subject", self.resource_path)))

    @odata(name="task", navigation=True)
    @property
    def task(self) -> Task:
        """Gets the task property"""
        return self.properties.get("task", Task(self.context, ResourcePath("task", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.TaskProcessingResult"

    @odata(name="workflowSubject")
    @property
    def workflow_subject(self) -> WorkflowSubject:
        """Gets the workflowSubject property"""
        return self.properties.get("workflowSubject", WorkflowSubject())
