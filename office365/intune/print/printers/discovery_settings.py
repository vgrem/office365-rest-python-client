from __future__ import annotations

from dataclasses import field

from office365.intune.print.air_print_settings import AirPrintSettings
from office365.runtime.client_value import ClientValue


class PrinterDiscoverySettings(ClientValue):
    airPrint: AirPrintSettings = field(default_factory=AirPrintSettings)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrinterDiscoverySettings"
