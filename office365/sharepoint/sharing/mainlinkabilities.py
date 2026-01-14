from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus
from office365.sharepoint.sharing.mainlinkaudienceabilities import (
    MainLinkAudienceAbilities,
)
from office365.sharepoint.sharing.mainlinkroleabilities import MainLinkRoleAbilities


class MainLinkAbilities(ClientValue):
    def __init__(
        self,
        can_get_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_reset_link: SharingAbilityStatus = SharingAbilityStatus(),
        main_link_audience_abilities: MainLinkAudienceAbilities = MainLinkAudienceAbilities(),
        main_link_role_abilities: MainLinkRoleAbilities = MainLinkRoleAbilities(),
    ):
        self.canGetLink = can_get_link
        self.canManageLink = can_manage_link
        self.canResetLink = can_reset_link
        self.mainLinkAudienceAbilities = main_link_audience_abilities
        self.mainLinkRoleAbilities = main_link_role_abilities

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkAbilities"
