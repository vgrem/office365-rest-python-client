from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.collection_position import ListCollectionPosition


@dataclass
class GetListsParameters(ClientValue):
    ListCollectionPosition: ListCollectionPosition = field(default_factory=ListCollectionPosition)
    RowLimit: int = 100

    @property
    def entity_type_name(self):
        return "SP.GetListsParameters"
