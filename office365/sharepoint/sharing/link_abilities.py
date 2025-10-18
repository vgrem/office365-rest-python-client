from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus
from office365.sharepoint.sharing.linkexpirationabilitystatus import (
    SharingLinkExpirationAbilityStatus,
)
from office365.sharepoint.sharing.linkpasswordabilitystatus import (
    SharingLinkPasswordAbilityStatus,
)


class SharingLinkAbilities(ClientValue):
    """
    Represents the set of capabilities for specific configurations of tokenized sharing link for the current user
    and whether they are enabled or not.
    """

    def __init__(
        self,
        can_add_new_external_principals=SharingAbilityStatus(),
        can_delete_edit_link=SharingAbilityStatus(),
        can_delete_manage_list_link=SharingAbilityStatus(),
        can_get_edit_link=SharingAbilityStatus(),
        can_get_read_link=SharingAbilityStatus(),
        can_delete_read_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_delete_restricted_view_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_delete_review_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_delete_submit_only_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_get_manage_list_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_get_restricted_view_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_get_review_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_get_submit_only_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_have_external_users: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_edit_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_manage_list_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_read_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_restricted_view_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_review_link: SharingAbilityStatus = SharingAbilityStatus(),
        can_manage_submit_only_link: SharingAbilityStatus = SharingAbilityStatus(),
        link_expiration: SharingLinkExpirationAbilityStatus = SharingLinkExpirationAbilityStatus(),
        password_protected: SharingLinkPasswordAbilityStatus = SharingLinkPasswordAbilityStatus(),
        submit_onlylink_expiration: SharingLinkExpirationAbilityStatus = SharingLinkExpirationAbilityStatus(),
        supports_restricted_view: SharingAbilityStatus = SharingAbilityStatus(),
        supports_restrict_to_existing_relationships: SharingAbilityStatus = SharingAbilityStatus(),
        track_link_users: SharingAbilityStatus = SharingAbilityStatus(),
    ):
        """
        :param SharingAbilityStatus can_add_new_external_principals:
        :param SharingAbilityStatus can_delete_edit_link:
        :param SharingAbilityStatus can_get_edit_link: Indicates whether the current user can get an existing tokenized
            sharing link that provides edit access.
        :param SharingAbilityStatus can_get_read_link: Indicates whether the current user can get an existing tokenized
            sharing link that provides read access.
        """
        self.canAddNewExternalPrincipals = can_add_new_external_principals
        self.canDeleteEditLink = can_delete_edit_link
        self.canDeleteManageListLink = can_delete_manage_list_link
        self.canGetEditLink = can_get_edit_link
        self.canGetReadLink = can_get_read_link
        self.canDeleteReadLink = can_delete_read_link
        self.canDeleteRestrictedViewLink = can_delete_restricted_view_link
        self.canDeleteReviewLink = can_delete_review_link
        self.canDeleteSubmitOnlyLink = can_delete_submit_only_link
        self.canGetManageListLink = can_get_manage_list_link
        self.canGetRestrictedViewLink = can_get_restricted_view_link
        self.canGetReviewLink = can_get_review_link
        self.canGetSubmitOnlyLink = can_get_submit_only_link
        self.canHaveExternalUsers = can_have_external_users
        self.canManageEditLink = can_manage_edit_link
        self.canManageManageListLink = can_manage_manage_list_link
        self.canManageReadLink = can_manage_read_link
        self.canManageRestrictedViewLink = can_manage_restricted_view_link
        self.canManageReviewLink = can_manage_review_link
        self.canManageSubmitOnlyLink = can_manage_submit_only_link
        self.linkExpiration = link_expiration
        self.passwordProtected = password_protected
        self.submitOnlylinkExpiration = submit_onlylink_expiration
        self.supportsRestrictedView = supports_restricted_view
        self.supportsRestrictToExistingRelationships = supports_restrict_to_existing_relationships
        self.trackLinkUsers = track_link_users

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkAbilities"
