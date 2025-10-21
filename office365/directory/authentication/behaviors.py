from office365.runtime.client_value import ClientValue


class AuthenticationBehaviors(ClientValue):

    def __init__(
        self,
        block_azure_ad_graph_access: bool = None,
        remove_unverified_email_claim: bool = None,
        require_client_service_principal: bool = None,
    ):
        self.blockAzureADGraphAccess = block_azure_ad_graph_access
        self.removeUnverifiedEmailClaim = remove_unverified_email_claim
        self.requireClientServicePrincipal = require_client_service_principal

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationBehaviors"
