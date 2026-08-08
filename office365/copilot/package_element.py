from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.json import Json


@dataclass
class PackageElement(ClientValue):
    definition: Json = field(default_factory=Json)
    id: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PackageElement"
