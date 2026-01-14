from office365.runtime.client_value import ClientValue


class SPOM365AgentInsightsSiteDistributionDetails(ClientValue):
    def __init__(
        self,
        agents: int = None,
        request_volume: int = None,
        sites: int = None,
        template: str = None,
    ):
        self.Agents = agents
        self.RequestVolume = request_volume
        self.Sites = sites
        self.Template = template

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsSiteDistributionDetails"
