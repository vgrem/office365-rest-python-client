from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TextColumn(ClientValue):
    """The textColumn on a columnDefinition resource indicates that the column's values are text."""

    maxLength: int | None = None
    allowMultipleLines: bool | None = None
    textType: str | None = None
