from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class BatchCreationResult(ClientValue):
    CreatedTaskIdList: StringCollection | None = None
    CreatedCount: int | None = None
    ErrorCode: str | None = None
    ErrorMessage: str | None = None
    FieldError: str | None = None
    ProcessingMilliseconds: int | None = None
    TotalCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.BatchCreationResult"
