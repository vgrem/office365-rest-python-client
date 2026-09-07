from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AccessReviewInstanceDecisionItemServicePrincipalResource(ClientValue):
    appId: str | None = None
    appRoleDisplayName: str | None = None
    appRoleId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemServicePrincipalResource"
