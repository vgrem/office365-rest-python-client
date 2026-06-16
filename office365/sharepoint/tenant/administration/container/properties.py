from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


@dataclass
class SPContainerProperties(ClientValue):
    AllowEditing: bool | None = None
    ArchivedBy: str | None = None
    ArchiveStatus: int | None = None
    AuthenticationContextName: str | None = None
    BlockDownloadPolicy: bool | None = None
    ConditionalAccessPolicy: int | None = None
    ContainerApiUrl: str | None = None
    ContainerId: str | None = None
    ContainerName: str | None = None
    ContainerSiteUrl: str | None = None
    ContainerTypeId: UUID | None = None
    CreatedBy: str | None = None
    CreatedOn: datetime | None = None
    Description: str | None = None
    ExcludeBlockDownloadPolicyContainerOwners: bool | None = None
    LastArchivedDateTime: datetime | None = None
    LimitedAccessFileType: int | None = None
    Managers: StringCollection | None = None
    NewPrincipalOwnerIdentifier: str | None = None
    Owners: StringCollection | None = None
    OwnersCount: int | None = None
    OwnershipType: str | None = None
    OwningApplicationId: UUID | None = None
    OwningApplicationName: str | None = None
    PrincipalOwnerIdentifier: str | None = None
    Readers: StringCollection | None = None
    ReadOnlyForBlockDownloadPolicy: bool | None = None
    ReadOnlyForUnmanagedDevices: bool | None = None
    SensitivityLabel: str | None = None
    SharingAllowedDomainList: str | None = None
    SharingBlockedDomainList: str | None = None
    SharingDomainRestrictionMode: int | None = None
    Status: str | None = None
    StorageUsed: int | None = None
    TransferFromPrincipalOwnerIdentifier: str | None = None
    Writers: StringCollection = field(default_factory=lambda: StringCollection())
    RestrictContentOrgWideSearch: bool | None = None
    ClearRestrictedAccessControl: bool | None = None
    ContainerRedirectUrl: str | None = None
    EnableRestrictedAccessControl: bool | None = None
    RestrictedAccessControlGroups: GuidCollection = field(default_factory=GuidCollection)
    RestrictedAccessControlGroupsToAdd: GuidCollection = field(default_factory=GuidCollection)
    RestrictedAccessControlGroupsToRemove: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerProperties"
