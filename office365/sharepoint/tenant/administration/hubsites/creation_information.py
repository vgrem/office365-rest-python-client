from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class HubSiteCreationInformation(ClientValue):
    Description: str | None = None
    EnablePermissionsSync: bool | None = None
    EnforcedECTs: str | None = None
    EnforcedECTsVersion: int | None = None
    HideNameInNavigation: bool | None = None
    LogoUrl: str | None = None
    ParentHubSiteId: str | None = None
    PermissionsSyncTag: int | None = None
    RequiresJoinApproval: bool | None = None
    SiteDesignId: str | None = None
    SiteId: str | None = None
    SiteUrl: str | None = None
    Targets: str | None = None
    TenantInstanceId: str | None = None
    Title: str | None = None
