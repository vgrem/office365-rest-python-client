from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus


@dataclass
class MainLinkRoleAbilities(ClientValue):
    commentRoleAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    editRoleAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    restrictedViewRoleAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    viewRoleAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkRoleAbilities"
