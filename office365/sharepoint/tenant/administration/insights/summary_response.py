from typing import Optional

from office365.runtime.client_value import ClientValue


class InsightsSummaryResponse(ClientValue):
    def __init__(self, insights_summary: Optional[str] = None, total_paged_count: Optional[int] = None):
        self.insightsSummary = insights_summary
        self.totalPagedCount = total_paged_count

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.InsightsSummaryResponse"
