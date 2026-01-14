from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class SPTenantIBInsightsReportSharePoint(Entity):
    @property
    def implicit(self) -> StringCollection:
        """Gets the Implicit property"""
        return self.properties.get("Implicit", StringCollection())

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Insights.SPTenantIBInsightsReportSharePoint"
