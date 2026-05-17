from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteCohortsSummary(ClientValue):
    def __init__(
        self,
        externally_shared_sites_count: Optional[int] = None,
        group_connected_sites_count: Optional[int] = None,
        inactive_sites_count: Optional[int] = None,
        total_sites_count: Optional[int] = None,
    ):
        self.ExternallySharedSitesCount = externally_shared_sites_count
        self.GroupConnectedSitesCount = group_connected_sites_count
        self.InactiveSitesCount = inactive_sites_count
        self.TotalSitesCount = total_sites_count

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCohortsSummary"
