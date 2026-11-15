from __future__ import annotations

from enum import Enum


class MicrosoftTunnelDeploymentMode(Enum):
    standaloneRootful = "0"
    standaloneRootless = "1"
    podRootful = "2"
    podRootless = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftTunnelDeploymentMode"
