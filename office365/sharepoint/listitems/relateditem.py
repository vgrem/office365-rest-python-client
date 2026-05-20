from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RelatedItem(ClientValue):
    icon_url: str | None = None
    item_id: int | None = None
    list_id: str | None = None
    title: str | None = None
    url: str | None = None
    web_id: str | None = None
