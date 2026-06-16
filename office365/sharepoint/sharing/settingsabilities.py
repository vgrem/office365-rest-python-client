from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus


@dataclass
class SharingSettingsAbilities(ClientValue):
    canGetBlockSharingPushDown: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canGetItemMembersCanShare: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageBlockSharingPushDown: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageItemMembersCanShare: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageBlockMembersCanShare: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageBlockSharingPushdown: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingSettingsAbilities"
