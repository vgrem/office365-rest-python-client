from office365.sharepoint.tenant.insights.reports.metadata import (
    SPTenantIBInsightsReportMetadata,
)


class SPTenantIBInsightsReport(SPTenantIBInsightsReportMetadata):
    """ """

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Insights.SPTenantIBInsightsReport"
