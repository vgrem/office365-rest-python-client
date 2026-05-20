from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class PersonOrGroupColumn(ClientValue):
    """The personOrGroupColumn on a columnDefinition resource indicates that the column's values represent
    a person or group chosen from the directory."""

    allowMultipleSelection: bool | None = None
    chooseFromType: str | None = None
    displayAs: str | None = None
