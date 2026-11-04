from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class RelatedItem(ClientValue):
    IconUrl: str | None = None
    ItemId: int | None = None
    ListId: str | None = None
    Title: str | None = None
    Url: str | None = None
    WebId: str | None = None
