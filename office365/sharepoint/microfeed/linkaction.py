from typing import Optional

from office365.runtime.client_value import ClientValue


class MicrofeedLinkAction(ClientValue):
    def __init__(
        self,
        action_uri: Optional[str] = None,
        height: Optional[int] = None,
        kind: Optional[int] = None,
        width: Optional[int] = None,
    ):
        self.ActionUri = action_uri
        self.Height = height
        self.Kind = kind
        self.Width = width

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedLinkAction"
