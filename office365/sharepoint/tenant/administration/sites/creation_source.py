from datetime import datetime
from typing import List

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.sites.creation_data import (
    SiteCreationData,
)


class SiteCreationSource(ClientValue):
    def __init__(
        self,
        is_sync_threshold_limit_reached: bool = None,
        last_refresh_time_stamp: datetime = None,
        site_creation_data: List[SiteCreationData] = None,
        sync_threshold_limit: int = None,
        total_sites_count: int = None,
    ) -> None:
        self.IsSyncThresholdLimitReached = is_sync_threshold_limit_reached
        self.LastRefreshTimeStamp = last_refresh_time_stamp
        self.SiteCreationData = ClientValueCollection(
            SiteCreationData, site_creation_data
        )
        self.SyncThresholdLimit = sync_threshold_limit
        self.TotalSitesCount = total_sites_count

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCreationSource"
