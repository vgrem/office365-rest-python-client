from __future__ import annotations

from dataclasses import field

from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.evidence.kubernetes_namespace import KubernetesNamespaceEvidence


class KubernetesSecretEvidence(AlertEvidence):
    name: str | None = None
    namespace: KubernetesNamespaceEvidence = field(default_factory=KubernetesNamespaceEvidence)
    secretType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesSecretEvidence"
