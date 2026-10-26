from __future__ import annotations

from dataclasses import dataclass

from office365.copilot.package_request_principal_type import CopilotPackageRequestPrincipalType
from office365.runtime.client_value import ClientValue


@dataclass
class CopilotPackageRequestPrincipal(ClientValue):
    principalType: CopilotPackageRequestPrincipalType = CopilotPackageRequestPrincipalType.user
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotPackageRequestPrincipal"
