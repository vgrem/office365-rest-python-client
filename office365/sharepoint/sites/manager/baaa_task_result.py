from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.baaa_task_result_details import BAAATaskResultDetails


class BAAATaskResult(ClientValue):
    ErrorCode: int | None = None
    ErrorMessage: str | None = None
    ResponseStatus: int | None = None
    TaskListId: UUID | None = None
    TaskListItemId: int | None = None
    TaskResultDetails: BAAATaskResultDetails = field(default_factory=BAAATaskResultDetails)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.BAAATaskResult"
