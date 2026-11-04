from __future__ import annotations

from office365.communications.calls.mediastate import MediaState
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CallMediaState(ClientValue):
    audio: MediaState = MediaState.active

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallMediaState"
