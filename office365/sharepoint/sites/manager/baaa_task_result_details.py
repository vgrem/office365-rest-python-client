from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.bulk_retire_task_result import BulkRetireTaskResult
from office365.sharepoint.sites.manager.scan_for_missing_links_task_result import ScanForMissingLinksTaskResult


class BAAATaskResultDetails(ClientValue):
    BulkRetire: BulkRetireTaskResult = field(default_factory=BulkRetireTaskResult)
    ScanForMissingLinks: ScanForMissingLinksTaskResult = field(default_factory=ScanForMissingLinksTaskResult)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.BAAATaskResultDetails"
