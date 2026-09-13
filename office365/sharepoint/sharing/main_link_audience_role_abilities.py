from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus


class MainLinkAudienceRoleAbilities(ClientValue):
    commentRoleAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    editRoleAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    restrictedViewRoleAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    viewRoleAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)

    @property
    def entity_type_name(self) -> str:
        return "SP.Sharing.MainLinkAudienceRoleAbilities"
