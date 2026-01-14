from office365.directory.authentication.methods.targettype import AuthenticationMethodTargetType
from office365.runtime.client_value import ClientValue


class AuthenticationMethodsRegistrationCampaignIncludeTarget(ClientValue):
    def __init__(
        self,
        id_: str = None,
        targeted_authentication_method: str = None,
        target_type: AuthenticationMethodTargetType = AuthenticationMethodTargetType.none,
    ):
        self.id = id_
        self.targetedAuthenticationMethod = targeted_authentication_method
        self.targetType = target_type

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodsRegistrationCampaignIncludeTarget"
