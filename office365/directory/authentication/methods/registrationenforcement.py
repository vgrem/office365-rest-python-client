from office365.directory.authentication.methods.registrationcampaign import (
    AuthenticationMethodsRegistrationCampaign as RegistrationCampaign,
)
from office365.runtime.client_value import ClientValue


class RegistrationEnforcement(ClientValue):

    def __init__(
        self,
        authentication_methods_registration_campaign: RegistrationCampaign = RegistrationCampaign(),
    ):
        self.authenticationMethodsRegistrationCampaign = authentication_methods_registration_campaign

    @property
    def entity_type_name(self):
        return "microsoft.graph.RegistrationEnforcement"
