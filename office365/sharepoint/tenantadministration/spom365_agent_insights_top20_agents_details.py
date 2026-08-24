from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SPOM365AgentInsightsTop20AgentsDetails(ClientValue):
    AgentName: str | None = None
    AgentType: str | None = None
    RequestVolume: int | None = None
    SitesAccessed: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsTop20AgentsDetails"
