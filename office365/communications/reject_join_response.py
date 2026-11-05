from __future__ import annotations

from office365.communications.calls.rejectreason import RejectReason
from office365.runtime.client_value import ClientValue


class RejectJoinResponse(ClientValue):
    reason: RejectReason = RejectReason.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RejectJoinResponse"
