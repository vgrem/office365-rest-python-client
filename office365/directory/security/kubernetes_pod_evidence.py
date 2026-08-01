from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.container_evidence import ContainerEvidence
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class KubernetesPodEvidence(ClientValue):
    containers: ClientValueCollection[ContainerEvidence] = field(
        default_factory=lambda: ClientValueCollection(ContainerEvidence)
    )
    ephemeralContainers: ClientValueCollection[ContainerEvidence] = field(
        default_factory=lambda: ClientValueCollection(ContainerEvidence)
    )
    initContainers: ClientValueCollection[ContainerEvidence] = field(
        default_factory=lambda: ClientValueCollection(ContainerEvidence)
    )
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesPodEvidence"
