from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TextColumn(ClientValue):
    """The textColumn on a columnDefinition resource indicates that the column's values are text."""

    maxLength: int | None = None
    allowMultipleLines: bool | None = None
    textType: str | None = None
    appendChangesToExistingText: bool | None = None
    linesForEditing: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TextColumn"
