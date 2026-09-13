from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus
from office365.sharepoint.sharing.main_link_audience_role_abilities import MainLinkAudienceRoleAbilities


@dataclass
class MainLinkAudienceAbilities(ClientValue):
    anyoneLinkAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    onlyPeopleAddedLinkAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    organizationLinkAvailable: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    anyone: MainLinkAudienceRoleAbilities = field(default_factory=MainLinkAudienceRoleAbilities)
    onlyPeopleAdded: SharingAbilityStatus = field(default_factory=SharingAbilityStatus)
    organization: MainLinkAudienceRoleAbilities = field(default_factory=MainLinkAudienceRoleAbilities)

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkAudienceAbilities"
