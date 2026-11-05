from __future__ import annotations

from dataclasses import field

from office365.communications.calls.recordingstatus import RecordingStatus
from office365.directory.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


class RecordingInfo(ClientValue):
    initiator: IdentitySet = field(default_factory=IdentitySet)
    recordingStatus: RecordingStatus = RecordingStatus.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RecordingInfo"
