from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.kubernetes_namespace_evidence import KubernetesNamespaceEvidence


@value
class KubernetesServiceAccountEvidence(ClientValue):
    name: str | None = None
    namespace: KubernetesNamespaceEvidence = field(default_factory=KubernetesNamespaceEvidence)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesServiceAccountEvidence"
