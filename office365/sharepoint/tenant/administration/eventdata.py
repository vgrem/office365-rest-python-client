from office365.runtime.client_value import ClientValue
from typing import Optional


class EventData(ClientValue):
    def __init__(
        self,
        archive_url: Optional[str] = None,
        group: Optional[str] = None,
        hub_site_id: Optional[str] = None,
        identity: Optional[str] = None,
        is_hub_site: Optional[str] = None,
        new_site_url: Optional[str] = None,
        previous_hub_site_id: Optional[str] = None,
        source_site_url: Optional[str] = None,
        storage_maximum_level: Optional[int] = None,
        storage_previous_maximum_level: Optional[int] = None,
        storage_previous_warning_level: Optional[int] = None,
        storage_warning_level: Optional[int] = None,
        target_site_url: Optional[str] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.EventData"
