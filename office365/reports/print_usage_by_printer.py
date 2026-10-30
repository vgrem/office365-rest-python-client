from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class PrintUsageByPrinter(Entity):
    @odata(name="printerId")
    @property
    def printer_id(self) -> Optional[str]:
        """Gets the printerId property"""
        return self.properties.get("printerId", None)

    @odata(name="printerName")
    @property
    def printer_name(self) -> Optional[str]:
        """Gets the printerName property"""
        return self.properties.get("printerName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintUsageByPrinter"
