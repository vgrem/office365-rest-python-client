from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.baaa_task_result import BAAATaskResult


class BAAAResponse(ClientValue):
    PageToken: str | None = None
    TaskResults: ClientValueCollection[BAAATaskResult] = field(
        default_factory=lambda: ClientValueCollection(BAAATaskResult)
    )
    WorkItemId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.BAAAResponse"
