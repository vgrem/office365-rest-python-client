from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


@dataclass
class SPContainerTypeConfigurationProperties(ClientValue):
    AnonymousLinkExpirationInDays: int | None = None
    ApplicationRedirectUrl: str | None = None
    Classification: int | None = None
    ContainerTypeId: UUID | None = None
    ContainerTypeName: str | None = None
    CopilotEmbeddedChatHosts: StringCollection = field(default_factory=lambda: StringCollection())
    IsDiscoverablilityDisabled: int | None = None
    IsMoveDisabled: int | None = None
    IsRenameDisabled: int | None = None
    IsSharingRestricted: int | None = None
    OverrideTenantWhoCanShareAnonymousAllowList: int | None = None
    OverrideTenantWhoCanShareAuthenticatedGuestAllowList: int | None = None
    OwningAppId: UUID | None = None
    WhoCanShareAnonymousAllowList: GuidCollection = field(default_factory=GuidCollection)
    WhoCanShareAuthenticatedGuestAllowList: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeConfigurationProperties"
