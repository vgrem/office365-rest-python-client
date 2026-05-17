from office365.sharepoint.tenant.insights.reports.metadata import (
    SPTenantIBInsightsReportMetadata,
)


class SPTenantIBInsightsReport(SPTenantIBInsightsReportMetadata):
    """ """

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Insights.SPTenantIBInsightsReport"
