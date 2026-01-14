from office365.directory.authentication.advancedconfigstate import AdvancedConfigState
from office365.directory.authentication.methods.featuretarget import FeatureTarget
from office365.runtime.client_value import ClientValue


class AuthenticationMethodFeatureConfiguration(ClientValue):
    def __init__(
        self,
        exclude_target: FeatureTarget = FeatureTarget(),
        include_target: FeatureTarget = FeatureTarget(),
        state: AdvancedConfigState = AdvancedConfigState.none,
    ):
        self.excludeTarget = exclude_target
        self.includeTarget = include_target
        self.state = state

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodFeatureConfiguration"
