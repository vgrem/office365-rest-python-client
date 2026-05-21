from __future__ import annotations

from typing import Optional
from uuid import UUID


from dataclasses import dataclass, field
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


@dataclass
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