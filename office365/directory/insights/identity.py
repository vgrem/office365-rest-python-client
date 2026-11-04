from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class InsightIdentity(ClientValue):
    """Complex type containing properties of sharedInsight items."""

    address: str | None = None

    displayName: str | None = None

    id: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InsightIdentity"
