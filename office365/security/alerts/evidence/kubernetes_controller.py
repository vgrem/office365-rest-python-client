from __future__ import annotations

from dataclasses import field

from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.evidence.kubernetes_namespace import KubernetesNamespaceEvidence
from office365.security.dictionary import Dictionary


class KubernetesControllerEvidence(AlertEvidence):
    labels: Dictionary = field(default_factory=Dictionary)
    name: str | None = None
    type: str | None = None
    namespace: KubernetesNamespaceEvidence = field(default_factory=KubernetesNamespaceEvidence)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesControllerEvidence"
