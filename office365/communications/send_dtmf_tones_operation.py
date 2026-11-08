from __future__ import annotations

from office365.communications.operations.senddtmfcompletionreason import SendDtmfCompletionReason
from office365.entity import Entity
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata


class SendDtmfTonesOperation(PollableOperation, Entity):
    @odata(name="completionReason")
    @property
    def completion_reason(self) -> SendDtmfCompletionReason:
        """Gets the completionReason property"""
        return self.properties.get("completionReason", SendDtmfCompletionReason.unknown)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SendDtmfTonesOperation"
