from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class GetSourceItemMetadataForODCMountPointRequest(ClientValue):
    IsCreateMountPointFlow: Optional[bool] = None
    MountedRemoteItemUniqueIds: GuidCollection = field(default_factory=GuidCollection)
    RemoteItemListId: Optional[UUID] = None
    RemoteItemSiteId: Optional[UUID] = None
    RemoteItemUniqueIds: GuidCollection = field(default_factory=GuidCollection)
    RemoteItemWebId: Optional[UUID] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.GetSourceItemMetadataForODCMountPointRequest"
