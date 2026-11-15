from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.runtime.types.collections import StringCollection
from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.evidence.container_image import ContainerImageEvidence

if TYPE_CHECKING:
    from office365.security.alerts.evidence.kubernetes_pod import (
        KubernetesPodEvidence,
    )


class ContainerEvidence(AlertEvidence):
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
