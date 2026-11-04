from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SiteCohortsSummary(ClientValue):
    ExternallySharedSitesCount: int | None = None
    GroupConnectedSitesCount: int | None = None
    InactiveSitesCount: int | None = None
    TotalSitesCount: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCohortsSummary"
