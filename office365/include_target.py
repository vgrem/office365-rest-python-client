from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class IncludeTarget(ClientValue):
    id: str | None = None
    targetType: AuthenticationMethodTargetType = AuthenticationMethodTargetType.user

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.IncludeTarget'