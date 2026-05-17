from typing import Optional

from office365.runtime.client_value import ClientValue


class SPOM365AgentInsightsM365AgentsOnSitesDetails(ClientValue):
    def __init__(
        self,
        agent_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        agent_type: Optional[str] = None,
        agent_version: Optional[str] = None,
        external_sharing: Optional[str] = None,
        request_volume: Optional[int] = None,
        restrict_site_access_enabled: Optional[str] = None,
        restrict_site_discovery_enabled: Optional[str] = None,
        sensitivity: Optional[str] = None,
        site_id: Optional[str] = None,
        site_name: Optional[str] = None,
        site_owner: Optional[str] = None,
        site_type: Optional[str] = None,
        site_url: Optional[str] = None,
        total_agents: Optional[int] = None,
        total_request_volume: Optional[int] = None,
    ):
        self.AgentID = agent_id
        self.AgentName = agent_name
        self.AgentType = agent_type
        self.AgentVersion = agent_version
        self.ExternalSharing = external_sharing
        self.RequestVolume = request_volume
        self.RestrictSiteAccessEnabled = restrict_site_access_enabled
        self.RestrictSiteDiscoveryEnabled = restrict_site_discovery_enabled
        self.Sensitivity = sensitivity
        self.SiteID = site_id
        self.SiteName = site_name
        self.SiteOwner = site_owner
        self.SiteType = site_type
        self.SiteURL = site_url
        self.TotalAgents = total_agents
        self.TotalRequestVolume = total_request_volume

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsM365AgentsOnSitesDetails"
