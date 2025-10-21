from office365.directory.authentication.advancedconfigstate import AdvancedConfigState
from office365.directory.authentication.methods.excludetarget import ExcludeTarget
from office365.directory.authentication.methods.registrationcampaignincludetarget import (
    AuthenticationMethodsRegistrationCampaignIncludeTarget,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class AuthenticationMethodsRegistrationCampaign(ClientValue):

    def __init__(
        self,
        exclude_targets: ClientValueCollection[ExcludeTarget] = ClientValueCollection(ExcludeTarget),
        include_targets: ClientValueCollection[
            AuthenticationMethodsRegistrationCampaignIncludeTarget
        ] = ClientValueCollection(AuthenticationMethodsRegistrationCampaignIncludeTarget),
        snooze_duration_in_days: int = None,
        state: AdvancedConfigState = AdvancedConfigState.none,
    ):
        self.excludeTargets = exclude_targets
        self.includeTargets = include_targets
        self.snoozeDurationInDays = snooze_duration_in_days
        self.state = state

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodsRegistrationCampaign"
