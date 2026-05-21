from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.transpilerresponse import (
    TranspilerResponse,
)


@dataclass
class CopilotTranspilerResponse(ClientValue):
    data: TranspilerResponse = field(default_factory=TranspilerResponse)
    errorMessage: str | None = None
    isEligible: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.CopilotTranspilerResponse"
