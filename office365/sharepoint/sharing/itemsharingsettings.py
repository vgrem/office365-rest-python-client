from typing import Optional

from office365.runtime.client_value import ClientValue


class ItemSharingSettings(ClientValue):
    def __init__(
        self,
        block_sharing_push_down: Optional[bool] = None,
        item_id: Optional[str] = None,
        item_members_can_share: Optional[bool] = None,
        item_name: Optional[str] = None,
        item_type: Optional[int] = None,
        parent_id: Optional[str] = None,
    ):
        self.blockSharingPushDown = block_sharing_push_down
        self.itemId = item_id
        self.itemMembersCanShare = item_members_can_share
        self.itemName = item_name
        self.itemType = item_type
        self.parentId = parent_id

    @property
    def entity_type_name(self):
        return "SP.Sharing.ItemSharingSettings"
