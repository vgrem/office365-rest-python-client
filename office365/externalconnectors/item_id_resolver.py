from __future__ import annotations

from dataclasses import field

from office365.externalconnectors.url_match_info import UrlMatchInfo
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ItemIdResolver(ClientValue):
    itemId: str | None = None
    urlMatchInfo: UrlMatchInfo = field(default_factory=UrlMatchInfo)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ItemIdResolver"
