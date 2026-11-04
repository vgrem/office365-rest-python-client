from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPListItemVersionChange(ClientValue):
    FieldTitle: str | None = None
    NewValue: str | None = None
    PreviousValue: str | None = None
