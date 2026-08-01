from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.dictionary import Dictionary
from office365.runtime.client_value import ClientValue


@dataclass
class KubernetesControllerEvidence(ClientValue):
    labels: Dictionary = field(default_factory=Dictionary)
    name: str | None = None
    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesControllerEvidence"
