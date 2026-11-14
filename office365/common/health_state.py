from __future__ import annotations

from enum import Enum


class HealthState(Enum):
    unknown = "0"
    healthy = "1"
    unhealthy = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.HealthState"
