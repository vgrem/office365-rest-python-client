from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus


class MainLinkAudienceAbilities(ClientValue):
    def __init__(
        self,
        anyone_link_available: SharingAbilityStatus = SharingAbilityStatus(),
        only_people_added_link_available: SharingAbilityStatus = SharingAbilityStatus(),
        organization_link_available: SharingAbilityStatus = SharingAbilityStatus(),
    ):
        self.anyoneLinkAvailable = anyone_link_available
        self.onlyPeopleAddedLinkAvailable = only_people_added_link_available
        self.organizationLinkAvailable = organization_link_available

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkAudienceAbilities"
