from __future__ import annotations

from enum import Enum


class CopilotPackageRequestPrincipalType(Enum):
    user = "0"
    group = "1"
    agentApplication = "2"
    agentUser = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotPackageRequestPrincipalType"
