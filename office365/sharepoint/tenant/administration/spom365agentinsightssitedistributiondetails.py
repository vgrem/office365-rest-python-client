from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPOM365AgentInsightsSiteDistributionDetails(ClientValue):
    Agents: int | None = None
    RequestVolume: int | None = None
    Sites: int | None = None
    Template: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsSiteDistributionDetails"
