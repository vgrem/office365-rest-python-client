from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class BatchDeletionResult(ClientValue):
    DeletedCount: Optional[int] = None
    DeletedTaskIdList: GuidCollection = field(default_factory=GuidCollection)
    ErrorCode: Optional[str] = None
    ErrorMessage: Optional[str] = None
    NotDeletedCount: Optional[int] = None
    NotDeletedTaskIdList: GuidCollection = field(default_factory=GuidCollection)
    ProcessingMilliseconds: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.BatchDeletionResult"
