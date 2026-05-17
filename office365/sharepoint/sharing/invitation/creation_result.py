from typing import Optional

from office365.runtime.client_value import ClientValue


class SPInvitationCreationResult(ClientValue):
    """Specifies a result of adding an invitation."""

    def __init__(
        self,
        email: Optional[str] = None,
        error: Optional[str] = None,
        invitation_link: Optional[str] = None,
        succeeded: Optional[bool] = None,
    ):
        super().__init__()
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
