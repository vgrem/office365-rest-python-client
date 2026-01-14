from office365.runtime.client_value import ClientValue


class SPOCopilotAgentInsightsTopSitesDetails(ClientValue):
    def __init__(
        self,
        copilot_agents: int = None,
        external_sharing: str = None,
        restrict_site_access_enabled: str = None,
        restrict_site_discovery_enabled: str = None,
        sensitivity: str = None,
        site_name: str = None,
        site_owner: str = None,
        template: str = None,
        url: str = None,
    ):
        self.CopilotAgents = copilot_agents
        self.ExternalSharing = external_sharing
        self.RestrictSiteAccessEnabled = restrict_site_access_enabled
        self.RestrictSiteDiscoveryEnabled = restrict_site_discovery_enabled
        self.Sensitivity = sensitivity
        self.SiteName = site_name
        self.SiteOwner = site_owner
        self.Template = template
        self.URL = url

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotAgentInsightsTopSitesDetails"
