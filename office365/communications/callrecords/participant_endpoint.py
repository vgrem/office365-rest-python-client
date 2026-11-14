from __future__ import annotations

from dataclasses import field

from office365.communications.callrecords.endpoint import Endpoint
from office365.communications.callrecords.user_feedback import UserFeedback
from office365.directory.permissions.identity import Identity
from office365.directory.permissions.identity_set import IdentitySet


class ParticipantEndpoint(Endpoint):
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
