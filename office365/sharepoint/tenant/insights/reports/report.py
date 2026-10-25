from __future__ import annotations

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.tenant.insights.reports.metadata import (
    SPTenantIBInsightsReportMetadata,
)


class SPTenantIBInsightsReport(SPTenantIBInsightsReportMetadata):
    """ """

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Insights.SPTenantIBInsightsReport"

    @odata(name="Explicit")
    @property
    def explicit(self) -> StringCollection:
        """Gets the Explicit property"""
        return self.properties.get("Explicit", StringCollection())

    @odata(name="ModeDistribution")
    @property
    def mode_distribution(self) -> StringCollection:
        """Gets the ModeDistribution property"""
        return self.properties.get("ModeDistribution", StringCollection())

    @odata(name="Open")
    @property
    def open(self) -> StringCollection:
        """Gets the Open property"""
        return self.properties.get("Open", StringCollection())

    @odata(name="OwnerModerated")
    @property
    def owner_moderated(self) -> StringCollection:
        """Gets the OwnerModerated property"""
        return self.properties.get("OwnerModerated", StringCollection())
