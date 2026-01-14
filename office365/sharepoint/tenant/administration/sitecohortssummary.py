from office365.runtime.client_value import ClientValue


class SiteCohortsSummary(ClientValue):
    def __init__(
        self,
        externally_shared_sites_count: int = None,
        group_connected_sites_count: int = None,
        inactive_sites_count: int = None,
        total_sites_count: int = None,
    ):
        self.ExternallySharedSitesCount = externally_shared_sites_count
        self.GroupConnectedSitesCount = group_connected_sites_count
        self.InactiveSitesCount = inactive_sites_count
        self.TotalSitesCount = total_sites_count

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCohortsSummary"
