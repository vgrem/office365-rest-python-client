from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class BatchCreationResult(ClientValue):
    CreatedCount = None
    CreatedTaskIdList: StringCollection | None = None
    ErrorCode = None
    ErrorMessage = None
    FieldError = None
    ProcessingMilliseconds = None
    TotalCount = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.BatchCreationResult"
