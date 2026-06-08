from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.listitems.versions.collection_position import (
    ListItemVersionCollectionPosition,
)


@dataclass
class GetListItemVersionsParameters(ClientValue):
    """Args:
        row_limit (int):
        sort_descending (bool):
    """

    RowLimit: int | None = None
    SortDescending: bool | None = None
    ListItemVersionCollectionPosition: ListItemVersionCollectionPosition = field(
        default_factory=ListItemVersionCollectionPosition
    )
