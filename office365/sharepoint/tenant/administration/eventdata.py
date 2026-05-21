from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class EventData(ClientValue):
    ArchiveUrl: str | None = None
    Group: str | None = None
    HubSiteId: str | None = None
    Identity: str | None = None
    IsHubSite: str | None = None
    NewSiteUrl: str | None = None
    PreviousHubSiteId: str | None = None
    SourceSiteUrl: str | None = None
    StorageMaximumLevel: int | None = None
    StoragePreviousMaximumLevel: int | None = None
    StoragePreviousWarningLevel: int | None = None
    StorageWarningLevel: int | None = None
    TargetSiteUrl: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.EventData"
