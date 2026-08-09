from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class OptionalClaim(ClientValue):
    additionalProperties: StringCollection = field(default_factory=StringCollection)
    essential: bool | None = None
    name: str | None = None
    source: str | None = None
    "Contains an optional claim associated with an application"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OptionalClaim"
