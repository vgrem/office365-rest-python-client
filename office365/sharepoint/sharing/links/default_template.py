from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.links.info import SharingLinkInfo


class SharingLinkDefaultTemplate(ClientValue):
    """"""

    def __init__(
        self,
        link_details=SharingLinkInfo(),
        password_protected: Optional[bool] = None,
        role: Optional[int] = None,
        scope: Optional[int] = None,
        share_kind: Optional[int] = None,
        track_link_users: Optional[bool] = None,
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
