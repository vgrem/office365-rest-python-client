from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ApplicationRiskScore(ClientValue):
    compliance: float | None = None
    legal: float | None = None
    provider: float | None = None
    security: float | None = None
    total: float | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskScore"
