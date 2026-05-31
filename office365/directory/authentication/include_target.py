from __future__ import annotations

from dataclasses import dataclass

from office365.directory.authentication.methods.targettype import AuthenticationMethodTargetType
from office365.runtime.client_value import ClientValue


@dataclass
class IncludeTarget(ClientValue):
    id: str | None = None
    targetType: AuthenticationMethodTargetType = AuthenticationMethodTargetType.user

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IncludeTarget"
