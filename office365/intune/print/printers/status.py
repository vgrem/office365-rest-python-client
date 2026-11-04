from __future__ import annotations

from dataclasses import field

from office365.intune.print.printers.processingstate import PrinterProcessingState
from office365.intune.print.printers.processingstatedetail import (
    PrinterProcessingStateDetail,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class PrinterStatus(ClientValue):
    description: str | None = None
    details: ClientValueCollection[PrinterProcessingStateDetail] = field(
        default_factory=lambda: ClientValueCollection(PrinterProcessingStateDetail)
    )
    state: PrinterProcessingState = PrinterProcessingState.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrinterStatus"
