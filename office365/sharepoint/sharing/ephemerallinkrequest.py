from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.links.share_settings import ShareLinkSettings


class EphemeralLinkRequest(ClientValue):
    def __init__(
        self,
        meeting_id: Optional[str] = None,
        people_picker_input: Optional[str] = None,
        settings: ShareLinkSettings = ShareLinkSettings(),
    ):
        self.meetingId = meeting_id
        self.peoplePickerInput = people_picker_input
        self.settings = settings

    @property
    def entity_type_name(self):
        return "SP.Sharing.EphemeralLinkRequest"
