from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AccessReviewInstanceDecisionItemCustomDataProvidedResource(ClientValue):
    customData: str | None = None
    scopeDisplayName: str | None = None
    scopeId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemCustomDataProvidedResource"
