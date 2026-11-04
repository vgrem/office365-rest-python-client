from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CollaborationInsightsOverview(ClientValue):
    lastReportDate: datetime | None = None
    totalGuests: int | None = None
    totalInternalUsers: int | None = None
    totalOneDrives: int | None = None
    totalSites: int | None = None
    totalUsers: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborationInsightsOverview"
