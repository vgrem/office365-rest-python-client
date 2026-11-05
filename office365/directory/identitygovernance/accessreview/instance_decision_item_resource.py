from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AccessReviewInstanceDecisionItemResource(ClientValue):
    displayName: str | None = None
    id: str | None = None
    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemResource"

    description: str | None = None
