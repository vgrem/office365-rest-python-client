from office365.runtime.client_value import ClientValue


class InsightsSummaryResponse(ClientValue):

    def __init__(self, insights_summary: str = None, total_paged_count: int = None):
        self.insightsSummary = insights_summary
        self.totalPagedCount = total_paged_count

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.InsightsSummaryResponse"
