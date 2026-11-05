from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AmazonResourceEvidence(ClientValue):
    amazonAccountId: str | None = None
    amazonResourceId: str | None = None
    resourceName: str | None = None
    resourceType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AmazonResourceEvidence"
