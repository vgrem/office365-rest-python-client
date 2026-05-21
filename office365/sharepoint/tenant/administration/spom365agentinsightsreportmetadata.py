from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPOM365AgentInsightsReportMetadata(ClientValue):
    CreatedDateTimeInUtc: str | None = None
    Id: UUID | None = None
    ReportPeriodInDays: int | None = None
    Status: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsReportMetadata"
