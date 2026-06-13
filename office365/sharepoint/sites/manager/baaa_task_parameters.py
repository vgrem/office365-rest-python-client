from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.bulk_retire_task_parameters import BulkRetireTaskParameters


class BAAATaskParameters(ClientValue):
    BulkRetire: BulkRetireTaskParameters = field(default_factory=BulkRetireTaskParameters)
    TaskType: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.BAAATaskParameters"
