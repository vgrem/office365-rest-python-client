from __future__ import annotations

from enum import Enum


class ConnectionOperationStatus(Enum):
    unspecified = "0"
    inprogress = "1"
    completed = "2"
    failed = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ConnectionOperationStatus"
