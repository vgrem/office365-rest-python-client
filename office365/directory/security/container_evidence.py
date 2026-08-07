from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.container_image_evidence import ContainerImageEvidence
from office365.directory.security.kubernetes_pod_evidence import KubernetesPodEvidence
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ContainerEvidence(ClientValue):
    args: StringCollection = field(default_factory=StringCollection)
    command: StringCollection = field(default_factory=StringCollection)
    containerId: str | None = None
    isPrivileged: bool | None = None
    name: str | None = None
    image: ContainerImageEvidence = field(default_factory=ContainerImageEvidence)
    pod: KubernetesPodEvidence = field(default_factory=KubernetesPodEvidence)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ContainerEvidence"
