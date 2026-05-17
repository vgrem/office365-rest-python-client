from office365.runtime.client_value import ClientValue
from typing import Optional


class SPOCopilotAgentInsightsSiteDistribution(ClientValue):
    def __init__(
        self, copilot_agents: Optional[int] = None, sites: Optional[int] = None, template: Optional[str] = None
    ):
        self.CopilotAgents = copilot_agents
        self.Sites = sites
        self.Template = template

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotAgentInsightsSiteDistribution"
