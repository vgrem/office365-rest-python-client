from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.emaildata import EmailData
from office365.sharepoint.sharing.links.share_settings import ShareLinkSettings


@dataclass
class ShareLinkRequest(ClientValue):
    """Represents a request for the retrieval or creation of a tokenized sharing link."""

    linkKind: int | None = None
    expiration: str | None = None
    peoplePickerInput: str | None = None
    settings: ShareLinkSettings | None = None
    createLink: bool = True
    emailData: EmailData = field(default_factory=EmailData)

    @property
    def entity_type_name(self):
        return "SP.Sharing.ShareLinkRequest"
