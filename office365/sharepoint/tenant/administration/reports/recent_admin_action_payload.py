from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class RecentAdminActionReportPayload(ClientValue):
    actions: str | None = None
    name: str | None = None
    queryEndDate: datetime | None = None
    queryStartDate: datetime | None = None
    reportType: int | None = None
    sites: str | None = None
    users: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.RecentAdminActionReportPayload"
