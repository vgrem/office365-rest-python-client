from __future__ import annotations

from office365.communications.callrecords.failurestage import FailureStage
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class FailureInfo(ClientValue):
    reason: str | None = None
    stage: FailureStage = FailureStage.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.FailureInfo"
