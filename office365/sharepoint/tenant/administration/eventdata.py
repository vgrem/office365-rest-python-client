from office365.runtime.client_value import ClientValue


class EventData(ClientValue):

    def __init__(
        self,
        archive_url: str = None,
        group: str = None,
        hub_site_id: str = None,
        identity: str = None,
        is_hub_site: str = None,
        new_site_url: str = None,
        previous_hub_site_id: str = None,
        source_site_url: str = None,
        storage_maximum_level: int = None,
        storage_previous_maximum_level: int = None,
        storage_previous_warning_level: int = None,
        storage_warning_level: int = None,
        target_site_url: str = None,
    ):
        self.ArchiveUrl = archive_url
        self.Group = group
        self.HubSiteId = hub_site_id
        self.Identity = identity
        self.IsHubSite = is_hub_site
        self.NewSiteUrl = new_site_url
        self.PreviousHubSiteId = previous_hub_site_id
        self.SourceSiteUrl = source_site_url
        self.StorageMaximumLevel = storage_maximum_level
        self.StoragePreviousMaximumLevel = storage_previous_maximum_level
        self.StoragePreviousWarningLevel = storage_previous_warning_level
        self.StorageWarningLevel = storage_warning_level
        self.TargetSiteUrl = target_site_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.EventData"
