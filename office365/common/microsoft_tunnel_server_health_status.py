from __future__ import annotations

from enum import Enum


class MicrosoftTunnelServerHealthStatus(Enum):
    unknown = "0"
    healthy = "1"
    unhealthy = "2"
    warning = "3"
    offline = "4"
    upgradeInProgress = "5"
    upgradeFailed = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftTunnelServerHealthStatus"
