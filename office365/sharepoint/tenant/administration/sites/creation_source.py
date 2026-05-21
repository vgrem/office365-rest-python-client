from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.sites.creation_data import (
    SiteCreationData,
)


@dataclass
class SiteCreationSource(ClientValue):
    IsSyncThresholdLimitReached: bool | None = None
    LastRefreshTimeStamp: datetime | None = None
    SiteCreationData: ClientValueCollection[SiteCreationData] = field(
        default_factory=lambda: ClientValueCollection(SiteCreationData)
    )
    SyncThresholdLimit: int | None = None
    TotalSitesCount: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCreationSource"
