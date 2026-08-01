from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.dictionary import Dictionary
from office365.directory.security.kubernetes_cluster_evidence import KubernetesClusterEvidence
from office365.runtime.client_value import ClientValue


@dataclass
class KubernetesNamespaceEvidence(ClientValue):
    cluster: KubernetesClusterEvidence = field(default_factory=KubernetesClusterEvidence)
    labels: Dictionary = field(default_factory=Dictionary)
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesNamespaceEvidence"
