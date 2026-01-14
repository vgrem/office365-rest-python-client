from office365.runtime.client_value import ClientValue


class SPOM365AgentInsightsM365AgentsOnSitesDetails(ClientValue):
    def __init__(
        self,
        agent_id: str = None,
        agent_name: str = None,
        agent_type: str = None,
        agent_version: str = None,
        external_sharing: str = None,
        request_volume: int = None,
        restrict_site_access_enabled: str = None,
        restrict_site_discovery_enabled: str = None,
        sensitivity: str = None,
        site_id: str = None,
        site_name: str = None,
        site_owner: str = None,
        site_type: str = None,
        site_url: str = None,
        total_agents: int = None,
        total_request_volume: int = None,
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
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsM365AgentsOnSitesDetails"
