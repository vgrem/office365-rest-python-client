from __future__ import annotations

from enum import Enum


class SnapshotJobStatus(Enum):
    notStarted = "0"
    running = "1"
    succeeded = "2"
    failed = "3"
    partiallySuccessful = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SnapshotJobStatus"
