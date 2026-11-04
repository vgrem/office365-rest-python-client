from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class IPv6Range(ClientValue):
    lowerAddress: str | None = None
    upperAddress: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IPv6Range"
