from __future__ import annotations

from typing import List, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WorkbookTableRow(Entity):
    """Represents a row in a table."""

    @odata(name="index")
    @property
    def index(self) -> Optional[int]:
        """Returns the index number of the row within the rows collection of the table. Zero-indexed."""
        return self.properties.get("index", None)

    @odata(name="values")
    @property
    def values(self) -> Optional[List]:
        """
        Represents the raw values of the specified range. The data returned could be of type string, number,
        or a boolean. Cell that contain an error will return the error string.
        """
        return self.properties.get("values", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookTableRow"
