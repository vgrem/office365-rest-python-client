from __future__ import annotations

from dataclasses import dataclass

from office365.directory.authentication.methods.targettype import AuthenticationMethodTargetType
from office365.runtime.client_value import ClientValue


@dataclass
class AuthenticationMethodsRegistrationCampaignIncludeTarget(ClientValue):
    id: str | None = None
    targetedAuthenticationMethod: str | None = None
    targetType: AuthenticationMethodTargetType = AuthenticationMethodTargetType.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodsRegistrationCampaignIncludeTarget"
