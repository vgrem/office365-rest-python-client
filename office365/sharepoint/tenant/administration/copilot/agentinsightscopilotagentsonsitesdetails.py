from typing import Optional

from office365.runtime.client_value import ClientValue


class SPOCopilotAgentInsightsCopilotAgentsOnSitesDetails(ClientValue):
    def __init__(
        self,
        copilot_name: Optional[str] = None,
        external_sharing: Optional[str] = None,
        restrict_site_access_enabled: Optional[str] = None,
        restrict_site_discovery_enabled: Optional[str] = None,
        sensitivity: Optional[str] = None,
        site_name: Optional[str] = None,
        site_owner: Optional[str] = None,
        template: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.CopilotName = copilot_name
        self.ExternalSharing = external_sharing
        self.RestrictSiteAccessEnabled = restrict_site_access_enabled
        self.RestrictSiteDiscoveryEnabled = restrict_site_discovery_enabled
        self.Sensitivity = sensitivity
        self.SiteName = site_name
        self.SiteOwner = site_owner
        self.Template = template
        self.URL = url

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotAgentInsightsCopilotAgentsOnSitesDetails"
