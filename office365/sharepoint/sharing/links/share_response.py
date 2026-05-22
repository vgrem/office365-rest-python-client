from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.links.info import SharingLinkInfo


@dataclass
class ShareLinkResponse(ClientValue):
    """
    Represents a response for a request for the retrieval or creation/update of a tokenized sharing link.
    """

    sharingLinkInfo: SharingLinkInfo = field(default_factory=SharingLinkInfo)

    def __str__(self):
        return self.sharingLinkInfo.Url or ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.ShareLinkResponse"
