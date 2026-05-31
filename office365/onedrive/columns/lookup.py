from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class LookupColumn(ClientValue):
    """
    The lookupColumn on a columnDefinition resource indicates that the column's values
    are looked up from another source in the site.
    """

    listId: str | None = None
    columnName: str | None = None
    allowMultipleValues: bool | None = None
    allowUnlimitedLength: bool | None = None
    primaryLookupColumnId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LookupColumn"
