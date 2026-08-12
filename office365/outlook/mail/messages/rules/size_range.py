from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SizeRange(ClientValue):
    maximumSize: int | None = None
    minimumSize: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SizeRange"
