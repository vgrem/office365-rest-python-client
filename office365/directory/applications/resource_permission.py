from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ResourcePermission(ClientValue):
    type: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResourcePermission"
