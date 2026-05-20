from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.advancedconfigstate import AdvancedConfigState
from office365.directory.authentication.methods.excludetarget import ExcludeTarget
from office365.directory.authentication.methods.registrationcampaignincludetarget import (
    AuthenticationMethodsRegistrationCampaignIncludeTarget,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AuthenticationMethodsRegistrationCampaign(ClientValue):
    excludeTargets: ClientValueCollection[ExcludeTarget] = field(
        default_factory=lambda: ClientValueCollection(ExcludeTarget)
    )
    includeTargets: ClientValueCollection[AuthenticationMethodsRegistrationCampaignIncludeTarget] = field(
        default_factory=lambda: ClientValueCollection(AuthenticationMethodsRegistrationCampaignIncludeTarget)
    )
    snoozeDurationInDays: int | None = None
    state: AdvancedConfigState = AdvancedConfigState.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodsRegistrationCampaign"
