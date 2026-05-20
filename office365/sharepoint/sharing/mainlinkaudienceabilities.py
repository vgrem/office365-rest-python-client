from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus


@dataclass
class MainLinkAudienceAbilities(ClientValue):
    anyoneLinkAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    onlyPeopleAddedLinkAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    organizationLinkAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkAudienceAbilities"
