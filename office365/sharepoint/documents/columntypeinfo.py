from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ColumnTypeInfo(ClientValue):
    PlaceholderId: str | None = None
    TranslatedPlaceholderType: str | None = None
