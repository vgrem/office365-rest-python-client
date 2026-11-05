from __future__ import annotations

from dataclasses import field

from office365.communications.callrecords.user_feedback import UserFeedback
from office365.directory.permissions.identity import Identity
from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


class ParticipantEndpoint(ClientValue):
    associatedIdentity: Identity = field(default_factory=Identity)
    cpuCoresCount: int | None = None
    cpuName: str | None = None
    cpuProcessorSpeedInMhz: int | None = None
    feedback: UserFeedback = field(default_factory=UserFeedback)
    identity: IdentitySet = field(default_factory=IdentitySet)
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.ParticipantEndpoint"
