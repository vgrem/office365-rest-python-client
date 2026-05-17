from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.recipientlimitsinfo import RecipientLimitsInfo


class RecipientLimits(ClientValue):
    def __init__(
        self,
        check_permissions: RecipientLimitsInfo = RecipientLimitsInfo(),
        grant_direct_access: RecipientLimitsInfo = RecipientLimitsInfo(),
        share_link: RecipientLimitsInfo = RecipientLimitsInfo(),
        share_link_with_defer_redeem: RecipientLimitsInfo = RecipientLimitsInfo(),
    ):
        self.checkPermissions = check_permissions
        self.grantDirectAccess = grant_direct_access
        self.shareLink = share_link
        self.shareLinkWithDeferRedeem = share_link_with_defer_redeem

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.RecipientLimits"
