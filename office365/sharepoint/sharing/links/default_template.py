from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.links.info import SharingLinkInfo


@dataclass
class SharingLinkDefaultTemplate(ClientValue):
    """"""

    linkDetails: SharingLinkInfo = field(default_factory=SharingLinkInfo)
    passwordProtected: bool | None = None
    role: int | None = None
    scope: int | None = None
    shareKind: int | None = None
    trackLinkUsers: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkDefaultTemplate"
