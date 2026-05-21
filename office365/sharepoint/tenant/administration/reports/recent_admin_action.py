from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class RecentAdminActionReport(ClientValue):
    actions: str | None = None
    createdByEmail: str | None = None
    createdByName: str | None = None
    createdDate: datetime | None = None
    downloadLink: str | None = None
    name: str | None = None
    numberOfRecords: int | None = None
    progressPercentage: float | None = None
    queryEndDate: datetime | None = None
    queryStartDate: datetime | None = None
    reportType: int | None = None
    requestId: str | None = None
    sites: str | None = None
    sPOCorrelationId: str | None = None
    status: int | None = None
    uALCorrelationId: str | None = None
    uALNumberOfRecords: int | None = None
    users: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.RecentAdminActionReport"
