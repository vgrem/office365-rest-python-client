from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ColumnTypeInfo(ClientValue):
    PlaceholderId: str | None = None
    TranslatedPlaceholderType: str | None = None
