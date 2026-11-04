from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.listitems.versions.collection_position import (
    ListItemVersionCollectionPosition,
)


@value
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
