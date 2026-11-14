from __future__ import annotations

from dataclasses import field

from office365.externalconnectors.url_match_info import UrlMatchInfo
from office365.externalconnectors.url_to_item_resolver_base import UrlToItemResolverBase


class ItemIdResolver(UrlToItemResolverBase):
    itemId: str | None = None
    urlMatchInfo: UrlMatchInfo = field(default_factory=UrlMatchInfo)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ItemIdResolver"
