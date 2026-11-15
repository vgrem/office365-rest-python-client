from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class SiteSuggestionItem(ClientValue):
    editor: str | None = None
    extension: str | None = None
    id: str | None = None
    itemType: str | None = None
    sortTime: datetime | None = field(default_factory=lambda: datetime.min)
    title: str | None = None
    url: str | None = None
