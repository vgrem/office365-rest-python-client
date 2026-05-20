from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.links.share_settings import ShareLinkSettings


@dataclass
class EphemeralLinkRequest(ClientValue):
    meetingId: str | None = None
    peoplePickerInput: str | None = None
    settings: ShareLinkSettings = field(default_factory=ShareLinkSettings)

    @property
    def entity_type_name(self):
        return "SP.Sharing.EphemeralLinkRequest"
