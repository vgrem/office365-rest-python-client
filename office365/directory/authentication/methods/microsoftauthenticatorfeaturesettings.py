from office365.directory.authentication.methods.featureconfiguration import (
    AuthenticationMethodFeatureConfiguration as FeatureConfiguration,
)
from office365.runtime.client_value import ClientValue


class MicrosoftAuthenticatorFeatureSettings(ClientValue):
    def __init__(
        self,
        display_app_information_required_state: FeatureConfiguration = FeatureConfiguration(),
        display_location_information_required_state: FeatureConfiguration = FeatureConfiguration(),
    ):
        self.displayAppInformationRequiredState = display_app_information_required_state
        self.displayLocationInformationRequiredState = display_location_information_required_state

    @property
    def entity_type_name(self):
        return "microsoft.graph.MicrosoftAuthenticatorFeatureSettings"
