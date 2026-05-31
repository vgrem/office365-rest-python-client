from office365.entity import Entity
from dataclasses import dataclass, field
from datetime import datetime
from office365.directory.identitygovernance.lifecycleworkflowprocessingstatus import LifecycleWorkflowProcessingStatus
from office365.runtime.paths.resource_path import ResourcePath
from typing import Optional

class TaskProcessingResult(Entity):

    @property
    def completed_date_time(self) -> datetime:
        """Gets the completedDateTime property"""
        return self.properties.get('completedDateTime', None)

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get('createdDateTime', None)

    @property
    def failure_reason(self) -> Optional[str]:
        """Gets the failureReason property"""
        return self.properties.get('failureReason', None)

    @property
    def processing_info(self) -> Optional[str]:
        """Gets the processingInfo property"""
        return self.properties.get('processingInfo', None)

    @property
    def processing_status(self) -> LifecycleWorkflowProcessingStatus:
        """Gets the processingStatus property"""
        return self.properties.get('processingStatus', LifecycleWorkflowProcessingStatus.queued)

    @property
    def started_date_time(self) -> datetime:
        """Gets the startedDateTime property"""
        return self.properties.get('startedDateTime', None)

    @property
    def subject(self) -> User:
        """Gets the subject property"""
        return self.properties.get('subject', User(self.context, ResourcePath('subject', self.resource_path)))

    @property
    def task(self) -> Task:
        """Gets the task property"""
        return self.properties.get('task', Task(self.context, ResourcePath('task', self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.identityGovernance.TaskProcessingResult'