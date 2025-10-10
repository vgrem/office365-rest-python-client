from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.links.info import SharingLinkInfo


class SharingLinkDefaultTemplate(ClientValue):
    """"""

    def __init__(
        self,
        link_details=SharingLinkInfo(),
        password_protected: bool = None,
        role: int = None,
        scope: int = None,
        share_kind: int = None,
        track_link_users: bool = None,
    ):
        self.linkDetails = link_details
        self.passwordProtected = password_protected
        self.role = role
        self.scope = scope
        self.shareKind = share_kind
        self.trackLinkUsers = track_link_users

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkDefaultTemplate"
