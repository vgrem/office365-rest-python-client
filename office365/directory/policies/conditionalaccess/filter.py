from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.filtermode import FilterMode
from office365.runtime.client_value import ClientValue


@dataclass
class ConditionalAccessFilter(ClientValue):
    mode: FilterMode = FilterMode.include
    rule: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessFilter"
