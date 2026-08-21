from __future__ import annotations

from dataclasses import dataclass

from office365.backuprestore.restoresessions.browse_query_response_item_type import BrowseQueryResponseItemType
from office365.runtime.client_value import ClientValue


@dataclass
class BrowseQueryResponseItem(ClientValue):
    itemKey: str | None = None
    itemsCount: int | None = None
    name: str | None = None
    sizeInBytes: str | None = None
    type: BrowseQueryResponseItemType = BrowseQueryResponseItemType.none
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowseQueryResponseItem"
