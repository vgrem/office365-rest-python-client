from __future__ import annotations

from office365.intune.print.operationprocessingstate import (
    PrintOperationProcessingState,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PrintOperationStatus(ClientValue):
    description: str | None = None
    state: PrintOperationProcessingState = PrintOperationProcessingState.notStarted

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintOperationStatus"
