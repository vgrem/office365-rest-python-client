from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MicrofeedDataQuery(ClientValue):

    def __init__(
        self,
        item_limit: int = None,
        query: str = None,
        view_fields: StringCollection = StringCollection(),
        view_fields_only: bool = None,
    ):
        self.ItemLimit = item_limit
        self.Query = query
        self.ViewFields = view_fields
        self.ViewFieldsOnly = view_fields_only

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedDataQuery"
