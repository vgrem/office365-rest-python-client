from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RelatedItem(ClientValue):
    IconUrl: str | None = None
    ItemId: int | None = None
    ListId: str | None = None
    Title: str | None = None
    Url: str | None = None
    WebId: str | None = None
