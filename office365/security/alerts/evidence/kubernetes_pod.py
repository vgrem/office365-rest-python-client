from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.evidence.ip import IpEvidence
from office365.security.alerts.evidence.kubernetes_controller import (
    KubernetesControllerEvidence,
)
from office365.security.alerts.evidence.kubernetes_namespace import (
    KubernetesNamespaceEvidence,
)
from office365.security.alerts.evidence.kubernetes_service_account import (
    KubernetesServiceAccountEvidence,
)
from office365.security.dictionary import Dictionary

if TYPE_CHECKING:
    from office365.security.alerts.evidence.container import ContainerEvidence


class KubernetesPodEvidence(AlertEvidence):
    containers: ClientValueCollection[ContainerEvidence] | None = None
    controller: KubernetesControllerEvidence = field(default_factory=KubernetesControllerEvidence)
    ephemeralContainers: ClientValueCollection[ContainerEvidence] | None = None
    initContainers: ClientValueCollection[ContainerEvidence] | None = None
    labels: Dictionary = field(default_factory=Dictionary)
    name: str | None = None
    namespace: KubernetesNamespaceEvidence = field(default_factory=KubernetesNamespaceEvidence)
    podIp: IpEvidence = field(default_factory=IpEvidence)
    serviceAccount: KubernetesServiceAccountEvidence = field(default_factory=KubernetesServiceAccountEvidence)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesPodEvidence"
