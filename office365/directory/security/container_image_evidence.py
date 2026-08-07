from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.container_registry_evidence import ContainerRegistryEvidence
from office365.runtime.client_value import ClientValue


@dataclass
class ContainerImageEvidence(ClientValue):
    imageId: str | None = None
    digestImage: ContainerImageEvidence | None = None
    registry: ContainerRegistryEvidence = field(default_factory=ContainerRegistryEvidence)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ContainerImageEvidence"
