from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPListItemVersionChange(ClientValue):
    FieldTitle: str | None = None
    NewValue: str | None = None
    PreviousValue: str | None = None
