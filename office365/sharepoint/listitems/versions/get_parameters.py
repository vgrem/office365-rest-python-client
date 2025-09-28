from office365.runtime.client_value import ClientValue
from office365.sharepoint.listitems.versions.collection_position import (
    ListItemVersionCollectionPosition,
)


class GetListItemVersionsParameters(ClientValue):
    """"""

    def __init__(
        self,
        row_limit: int = None,
        sort_descending: bool = None,
        list_item_version_collection_position: ListItemVersionCollectionPosition = ListItemVersionCollectionPosition(),
    ):
        """
        :param int row_limit:
        :param bool sort_descending:
        """
        self.RowLimit = row_limit
        self.SortDescending = sort_descending
        self.ListItemVersionCollectionPosition = list_item_version_collection_position
