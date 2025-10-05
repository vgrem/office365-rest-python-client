from office365.runtime.client_value import ClientValue


class SocialAttachmentAction(ClientValue):

    def __init__(
        self,
        action_kind: int = None,
        action_uri: str = None,
        height: int = None,
        width: int = None,
    ):
        """The SocialAttachmentAction class specifies the user actions that are allowed for the attachment object."""
        self.ActionKind = action_kind
        self.ActionUri = action_uri
        self.Height = height
        self.Width = width

    @property
    def entity_type_name(self):
        return "SP.Social.SocialAttachmentAction"
