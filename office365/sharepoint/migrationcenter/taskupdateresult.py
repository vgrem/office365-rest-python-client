from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class TaskUpdateResult(ClientValue):
    def __init__(self, error_code: Optional[str] = None, task_id: Optional[UUID] = None):
        self.ErrorCode = error_code
        self.TaskId = task_id

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.TaskUpdateResult"
