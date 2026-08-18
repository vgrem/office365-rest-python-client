from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class PrintUsageByPrinter(Entity):
    @property
    def printer_id(self) -> Optional[str]:
        """Gets the printerId property"""
        return self.properties.get("printerId", None)

    @property
    def printer_name(self) -> Optional[str]:
        """Gets the printerName property"""
        return self.properties.get("printerName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintUsageByPrinter"
