from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value
from office365.security.container_image_evidence import ContainerImageEvidence

if TYPE_CHECKING:
    from office365.security.kubernetes_pod_evidence import (
        KubernetesPodEvidence,
    )


@value
class ContainerEvidence(ClientValue):
    args: StringCollection = field(default_factory=StringCollection)
    command: StringCollection = field(default_factory=StringCollection)
    containerId: str | None = None
    image: ContainerImageEvidence = field(default_factory=ContainerImageEvidence)
    isPrivileged: bool | None = None
    name: str | None = None
    pod: KubernetesPodEvidence | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ContainerEvidence"
