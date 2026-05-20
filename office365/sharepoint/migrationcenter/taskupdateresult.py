from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class TaskUpdateResult(ClientValue):
    ErrorCode: Optional[str] = None
    TaskId: Optional[UUID] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.TaskUpdateResult"
