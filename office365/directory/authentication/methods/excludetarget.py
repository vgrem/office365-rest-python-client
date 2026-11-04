from __future__ import annotations

from office365.directory.authentication.methods.targettype import AuthenticationMethodTargetType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ExcludeTarget(ClientValue):
    id: str | None = None
    targetType: AuthenticationMethodTargetType = AuthenticationMethodTargetType.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.ExcludeTarget"
