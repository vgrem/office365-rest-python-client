from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteCohortsSummary(ClientValue):
    ExternallySharedSitesCount: int | None = None
    GroupConnectedSitesCount: int | None = None
    InactiveSitesCount: int | None = None
    TotalSitesCount: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCohortsSummary"
