from __future__ import annotations

from enum import Enum


class ActivationUserScopeType(Enum):
    allUsers = "0"
    failedUsers = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.ActivationUserScopeType"
