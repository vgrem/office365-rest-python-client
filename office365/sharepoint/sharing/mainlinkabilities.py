from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus
from office365.sharepoint.sharing.mainlinkaudienceabilities import (
    MainLinkAudienceAbilities,
)
from office365.sharepoint.sharing.mainlinkroleabilities import MainLinkRoleAbilities


@dataclass
class MainLinkAbilities(ClientValue):
    canGetLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canManageLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    canResetLink: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    mainLinkAudienceAbilities: MainLinkAudienceAbilities = field(default_factory=MainLinkAudienceAbilities)
    mainLinkRoleAbilities: MainLinkRoleAbilities = field(default_factory=MainLinkRoleAbilities)

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkAbilities"
