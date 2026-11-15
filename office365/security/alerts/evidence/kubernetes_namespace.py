from __future__ import annotations

from dataclasses import field

from office365.security.alerts.dictionary import Dictionary
from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.evidence.kubernetes_cluster import KubernetesClusterEvidence


class KubernetesNamespaceEvidence(AlertEvidence):
    cluster: KubernetesClusterEvidence = field(default_factory=KubernetesClusterEvidence)
    labels: Dictionary = field(default_factory=Dictionary)
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesNamespaceEvidence"
