from __future__ import annotations

from dataclasses import dataclass

from office365.directory.security.containerportprotocol import ContainerPortProtocol
from office365.runtime.client_value import ClientValue


@dataclass
class KubernetesServicePort(ClientValue):
    appProtocol: str | None = None
    name: str | None = None
    nodePort: int | None = None
    port: int | None = None
    protocol: ContainerPortProtocol = ContainerPortProtocol.udp
    targetPort: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.KubernetesServicePort"
