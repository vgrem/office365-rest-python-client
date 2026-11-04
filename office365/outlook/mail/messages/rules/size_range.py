from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SizeRange(ClientValue):
    maximumSize: int | None = None
    minimumSize: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SizeRange"
