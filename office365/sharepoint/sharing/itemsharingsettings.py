from office365.runtime.client_value import ClientValue


class ItemSharingSettings(ClientValue):
    def __init__(
        self,
        block_sharing_push_down: bool = None,
        item_id: str = None,
        item_members_can_share: bool = None,
        item_name: str = None,
        item_type: int = None,
        parent_id: str = None,
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
