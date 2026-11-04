from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AlteredQueryToken(ClientValue):
    length: int | None = None
    offset: int | None = None
    suggestion: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AlteredQueryToken"
