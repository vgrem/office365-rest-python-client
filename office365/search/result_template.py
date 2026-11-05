from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.json import Json


class ResultTemplate(ClientValue):
    body: Json = field(default_factory=Json)
    displayName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResultTemplate"
