from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


class GetRemoteItemInfoRequest(ClientValue):
    def __init__(
        self,
        remote_item_unique_ids=None,
        is_create_mount_point_flow: Optional[bool] = None,
        mounted_remote_item_unique_ids: GuidCollection = GuidCollection(),
        remote_item_list_id: Optional[UUID] = None,
        remote_item_site_id: Optional[UUID] = None,
        remote_item_web_id: Optional[UUID] = None,
    ):
        self.RemoteItemUniqueIds = StringCollection(remote_item_unique_ids)
        self.IsCreateMountPointFlow = is_create_mount_point_flow
        self.MountedRemoteItemUniqueIds = mounted_remote_item_unique_ids
        self.RemoteItemListId = remote_item_list_id
        self.RemoteItemSiteId = remote_item_site_id
        self.RemoteItemWebId = remote_item_web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.GetRemoteItemInfoRequest"
