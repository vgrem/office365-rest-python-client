from office365.runtime.client_value import ClientValue


class SPOCopilotAgentInsightsSiteDistribution(ClientValue):

    def __init__(self, copilot_agents: int = None, sites: int = None, template: str = None):
        self.CopilotAgents = copilot_agents
        self.Sites = sites
        self.Template = template

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotAgentInsightsSiteDistribution"
