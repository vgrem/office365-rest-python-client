from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.mitre_technique import MitreTechnique


@dataclass
class MitreTactic(ClientValue):
    tactic: str | None = None
    techniques: ClientValueCollection[MitreTechnique] = field(
        default_factory=lambda: ClientValueCollection(MitreTechnique)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.MitreTactic"
