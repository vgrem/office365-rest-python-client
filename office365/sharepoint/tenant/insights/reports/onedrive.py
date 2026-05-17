from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class SPTenantIBInsightsReportOneDrive(Entity):
    @property
    def mixed(self) -> StringCollection:
        """Gets the Mixed property"""
        return self.properties.get("Mixed", StringCollection())

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Insights.SPTenantIBInsightsReportOneDrive"
