from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class CampaignPublicationResetEndpointParam(ClientValue):

    def __init__(
        self,
        email_transpile_content: str = None,
        engage_transpile_content: str = None,
        reset_endpoint: StringCollection = StringCollection(),
        teams_transpile_content: str = None,
    ):
        self.EmailTranspileContent = email_transpile_content
        self.EngageTranspileContent = engage_transpile_content
        self.ResetEndpoint = reset_endpoint
        self.TeamsTranspileContent = teams_transpile_content

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationResetEndpointParam"
