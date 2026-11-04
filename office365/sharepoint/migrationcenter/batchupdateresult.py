from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.migrationcenter.taskupdateresult import TaskUpdateResult


@value
class BatchUpdateResult(ClientValue):
    ErrorCode: Optional[str] = None
    FailCount: Optional[int] = None
    ProcessingMilliseconds: Optional[int] = None
    ResultList: ClientValueCollection[TaskUpdateResult] = field(
        default_factory=lambda: ClientValueCollection(TaskUpdateResult)
    )
    SuccessCount: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.BatchUpdateResult"
