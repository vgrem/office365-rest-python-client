from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus


class MainLinkRoleAbilities(ClientValue):
    def __init__(
        self,
        comment_role_available: SharingAbilityStatus = SharingAbilityStatus(),
        edit_role_available: SharingAbilityStatus = SharingAbilityStatus(),
        restricted_view_role_available: SharingAbilityStatus = SharingAbilityStatus(),
        view_role_available: SharingAbilityStatus = SharingAbilityStatus(),
    ):
        self.commentRoleAvailable = comment_role_available
        self.editRoleAvailable = edit_role_available
        self.restrictedViewRoleAvailable = restricted_view_role_available
        self.viewRoleAvailable = view_role_available

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkRoleAbilities"
