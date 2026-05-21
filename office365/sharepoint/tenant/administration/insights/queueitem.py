from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class InsightsQueueItem(ClientValue):
    insightsCompletionTime: datetime | None = None
    insightsScenario: int | None = None
    itemId: int | None = None
    reportCreationTime: datetime | None = None
    reportDataFileName: str | None = None
    reportId: str | None = None
    status: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.InsightsQueueItem"
