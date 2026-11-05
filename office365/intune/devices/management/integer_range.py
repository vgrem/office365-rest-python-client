from __future__ import annotations

from office365.runtime.client_value import ClientValue


class IntegerRange(ClientValue):
    end: int | None = None
    start: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IntegerRange"
