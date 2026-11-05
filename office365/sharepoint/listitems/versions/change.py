from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SPListItemVersionChange(ClientValue):
    FieldTitle: str | None = None
    NewValue: str | None = None
    PreviousValue: str | None = None
