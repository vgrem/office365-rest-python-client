from __future__ import annotations

from dataclasses import field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MeetingParticipantInfo(ClientValue):
    """Information about a participant in a meeting.

    Fields:
        identity: Identity information of the participant.
        role: Specifies the participant's role in the meeting.
        upn: User principal name of the participant.
    """

    identity: IdentitySet = field(default_factory=IdentitySet)
    role: str | None = None
    upn: str | None = None
