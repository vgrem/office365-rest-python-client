from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.teams.members.open_complex_dictionary_type import OpenComplexDictionaryType


@dataclass
class BaselineResource(ClientValue):
    displayName: str | None = None
    properties: OpenComplexDictionaryType = field(default_factory=OpenComplexDictionaryType)
    resourceType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BaselineResource"
