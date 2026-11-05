from __future__ import annotations

from office365.runtime.client_value import ClientValue


class Diagnostic(ClientValue):
    message: str | None = None
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Diagnostic"
