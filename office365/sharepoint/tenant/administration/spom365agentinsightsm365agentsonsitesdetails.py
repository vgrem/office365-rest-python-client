from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPOM365AgentInsightsM365AgentsOnSitesDetails(ClientValue):
    AgentID: str | None = None
    AgentName: str | None = None
    AgentType: str | None = None
    AgentVersion: str | None = None
    ExternalSharing: str | None = None
    RequestVolume: int | None = None
    RestrictSiteAccessEnabled: str | None = None
    RestrictSiteDiscoveryEnabled: str | None = None
    Sensitivity: str | None = None
    SiteID: str | None = None
    SiteName: str | None = None
    SiteOwner: str | None = None
    SiteType: str | None = None
    SiteURL: str | None = None
    TotalAgents: int | None = None
    TotalRequestVolume: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsM365AgentsOnSitesDetails"
