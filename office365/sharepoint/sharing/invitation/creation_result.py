from office365.runtime.client_value import ClientValue


class SPInvitationCreationResult(ClientValue):
    """Specifies a result of adding an invitation."""

    def __init__(
        self,
        email: str = None,
        error: str = None,
        invitation_link: str = None,
        succeeded: bool = None,
    ):
        super(SPInvitationCreationResult, self).__init__()
        "\n        "
        self.Email = None
        self.InvitationLink = None
        self.Succeeded = None
        self.Email = email
        self.Error = error
        self.InvitationLink = invitation_link
        self.Succeeded = succeeded

    @property
    def entity_type_name(self):
        return "SP.SPInvitationCreationResult"
