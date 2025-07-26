from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class WorkbookRangeView(Entity):
    """Represents a set of visible cells of the parent range."""

    @property
    def cell_addresses(self) -> Optional[dict]:
        """The cell addresses."""
        return self.properties.get("cellAddresses", None)

    @property
    def column_count(self) -> Optional[int]:
        """The number of visible columns."""
        return self.properties.get("columnCount", None)

    @property
    def rows(self) -> EntityCollection[WorkbookRangeView]:
        """Represents a collection of range views associated with the range."""
        return self.properties.get(
            "rows",
            EntityCollection(
                self.context,
                WorkbookRangeView,
                ResourcePath("rows", self.resource_path),
            ),
        )
