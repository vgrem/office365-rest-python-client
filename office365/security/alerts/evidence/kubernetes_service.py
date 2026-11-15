from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.alerts.dictionary import Dictionary
from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.evidence.ip import IpEvidence
from office365.security.alerts.evidence.kubernetes_namespace import KubernetesNamespaceEvidence
from office365.security.alerts.kubernetesservicetype import KubernetesServiceType
from office365.security.iot.kubernetes_service_port import KubernetesServicePort


class KubernetesServiceEvidence(AlertEvidence):
    clusterIP: IpEvidence = field(default_factory=IpEvidence)
    externalIPs: ClientValueCollection[IpEvidence] = field(default_factory=lambda: ClientValueCollection(IpEvidence))
    labels: Dictionary = field(default_factory=Dictionary)
    name: str | None = None
    namespace: KubernetesNamespaceEvidence = field(default_factory=KubernetesNamespaceEvidence)
    selector: Dictionary = field(default_factory=Dictionary)
    servicePorts: ClientValueCollection[KubernetesServicePort] = field(
        default_factory=lambda: ClientValueCollection(KubernetesServicePort)
    )
    serviceType: KubernetesServiceType = KubernetesServiceType.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesServiceEvidence"
