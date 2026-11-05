from __future__ import annotations

from office365.runtime.client_value import ClientValue


class UrlEvidence(ClientValue):
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.UrlEvidence"
