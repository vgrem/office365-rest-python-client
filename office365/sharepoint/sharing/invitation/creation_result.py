from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPInvitationCreationResult(ClientValue):
    """Specifies a result of adding an invitation."""

    Email: str | None = None
    Error: str | None = None
    InvitationLink: str | None = None
    Succeeded: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.SPInvitationCreationResult"
