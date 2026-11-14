from __future__ import annotations

from office365.copilot.package_request_principal_type import CopilotPackageRequestPrincipalType
from office365.directory.permissions.identity import Identity


class CopilotPackageRequestPrincipal(Identity):
    principalType: CopilotPackageRequestPrincipalType = CopilotPackageRequestPrincipalType.user
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotPackageRequestPrincipal"
