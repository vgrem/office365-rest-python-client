from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class MetaDataKeyValuePair(ClientValue):
    key: str | None = None
    value: dict = field(default_factory=dict)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MetaDataKeyValuePair"
