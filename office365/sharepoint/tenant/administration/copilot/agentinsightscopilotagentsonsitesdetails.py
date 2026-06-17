from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPOCopilotAgentInsightsCopilotAgentsOnSitesDetails(ClientValue):
    CopilotName: str | None = None
    ExternalSharing: str | None = None
    RestrictSiteAccessEnabled: str | None = None
    RestrictSiteDiscoveryEnabled: str | None = None
    Sensitivity: str | None = None
    SiteName: str | None = None
    SiteOwner: str | None = None
    Template: str | None = None
    URL: str | None = None
    AgentCreatedDate: str | None = None
    CreatedBy: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotAgentInsightsCopilotAgentsOnSitesDetails"
