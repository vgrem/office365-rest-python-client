from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SPDataGovernanceInsightQueryParameters(ClientValue):
    IncludeWorkload: bool | None = None
    ReportEntity: int | None = None
    Workload: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightQueryParameters"
