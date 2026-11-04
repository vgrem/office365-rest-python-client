from __future__ import annotations

from dataclasses import field

from office365.intune.print.printers.discovery_settings import PrinterDiscoverySettings
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PrintSettings(ClientValue):
    documentConversionEnabled: bool | None = None
    printerDiscoverySettings: PrinterDiscoverySettings = field(default_factory=PrinterDiscoverySettings)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintSettings"
