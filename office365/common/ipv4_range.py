from __future__ import annotations

from office365.runtime.client_value import ClientValue


class IPv4Range(ClientValue):
    lowerAddress: str | None = None
    upperAddress: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IPv4Range"
