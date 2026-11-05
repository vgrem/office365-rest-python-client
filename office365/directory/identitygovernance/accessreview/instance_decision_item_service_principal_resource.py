from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AccessReviewInstanceDecisionItemServicePrincipalResource(ClientValue):
    appId: str | None = None
    appRoleDisplayName: str | None = None
    appRoleId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemServicePrincipalResource"
