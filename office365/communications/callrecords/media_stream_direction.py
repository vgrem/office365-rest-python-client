from __future__ import annotations

from enum import Enum


class MediaStreamDirection(Enum):
    callerToCallee = "0"
    calleeToCaller = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.MediaStreamDirection"
