from office365.runtime.client_value import ClientValue
from typing import Optional


class SPOM365AgentInsightsSiteDistributionDetails(ClientValue):
    def __init__(
        self,
        agents: Optional[int] = None,
        request_volume: Optional[int] = None,
        sites: Optional[int] = None,
        template: Optional[str] = None,
    ):
        self.Agents = agents
        self.RequestVolume = request_volume
        self.Sites = sites
        self.Template = template

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsSiteDistributionDetails"
