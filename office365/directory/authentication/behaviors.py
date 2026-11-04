from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AuthenticationBehaviors(ClientValue):
    blockAzureADGraphAccess: bool | None = None
    removeUnverifiedEmailClaim: bool | None = None
    requireClientServicePrincipal: bool | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationBehaviors"

    coopEnforcement: bool | None = None
