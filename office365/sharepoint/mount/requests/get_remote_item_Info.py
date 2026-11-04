from __future__ import annotations

from dataclasses import field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection
from office365.runtime.types.value import value


@value
class GetRemoteItemInfoRequest(ClientValue):
    RemoteItemUniqueIds: StringCollection | None = None
    IsCreateMountPointFlow: Optional[bool] = None
    MountedRemoteItemUniqueIds: GuidCollection = field(default_factory=GuidCollection)
    RemoteItemListId: Optional[UUID] = None
    RemoteItemSiteId: Optional[UUID] = None
    RemoteItemWebId: Optional[UUID] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.GetRemoteItemInfoRequest"
