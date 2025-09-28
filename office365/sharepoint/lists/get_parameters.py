from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.collection_position import ListCollectionPosition


class GetListsParameters(ClientValue):

    def __init__(
        self,
        position=ListCollectionPosition(),
        row_limit: int = 100,
        list_collection_position: ListCollectionPosition = ListCollectionPosition(),
    ):
        self.ListCollectionPosition = position
        self.RowLimit = row_limit
        self.ListCollectionPosition = list_collection_position

    @property
    def entity_type_name(self):
        return "SP.GetListsParameters"
