from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class InsightsSummaryResponse(ClientValue):
    insightsSummary: str | None = None
    totalPagedCount: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.InsightsSummaryResponse"
