from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.methods.registrationcampaign import (
    AuthenticationMethodsRegistrationCampaign as RegistrationCampaign,
)
from office365.runtime.client_value import ClientValue


@dataclass
class RegistrationEnforcement(ClientValue):
    authenticationMethodsRegistrationCampaign: RegistrationCampaign = field(default_factory=RegistrationCampaign)

    @property
    def entity_type_name(self):
        return "microsoft.graph.RegistrationEnforcement"
