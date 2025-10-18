from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus


class SharingSettingsAbilities(ClientValue):

    def __init__(
        self,
        can_get_block_sharing_push_down: SharingAbilityStatus = SharingAbilityStatus(),
        can_get_item_members_can_share: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_block_sharing_push_down: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_item_members_can_share: SharingAbilityStatus = SharingAbilityStatus(),
    ):
        self.canGetBlockSharingPushDown = can_get_block_sharing_push_down
        self.canGetItemMembersCanShare = can_get_item_members_can_share
        self.canManageBlockSharingPushDown = can_manage_block_sharing_push_down
        self.canManageItemMembersCanShare = can_manage_item_members_can_share

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingSettingsAbilities"
