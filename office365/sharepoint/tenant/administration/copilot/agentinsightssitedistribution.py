from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPOCopilotAgentInsightsSiteDistribution(ClientValue):
    CopilotAgents: int | None = None
    Sites: int | None = None
    Template: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotAgentInsightsSiteDistribution"
