from __future__ import annotations

from office365.runtime.client_value import ClientValue


class IntegratedApplicationMetadata(ClientValue):
    name: str | None = None
    version: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IntegratedApplicationMetadata"
