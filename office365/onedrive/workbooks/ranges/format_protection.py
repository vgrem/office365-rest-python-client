from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WorkbookFormatProtection(Entity):
    """Represents the format protection of a range object."""

    @odata(name="formulaHidden")
    @property
    def formula_hidden(self) -> Optional[bool]:
        """Gets the formulaHidden property"""
        return self.properties.get("formulaHidden", None)

    @odata(name="locked")
    @property
    def locked(self) -> Optional[bool]:
        """Gets the locked property"""
        return self.properties.get("locked", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookFormatProtection"
