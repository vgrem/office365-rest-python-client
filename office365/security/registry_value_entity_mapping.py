from __future__ import annotations

from office365.runtime.client_value import ClientValue


class RegistryValueEntityMapping(ClientValue):
    keyColumn: str | None = None
    valueNameColumn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.RegistryValueEntityMapping"
