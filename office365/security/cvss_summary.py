from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.vulnerability_severity import VulnerabilitySeverity


@value
class CvssSummary(ClientValue):
    score: float | None = None
    vectorString: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.CvssSummary"

    severity: VulnerabilitySeverity = VulnerabilitySeverity.none
