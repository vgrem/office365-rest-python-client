from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MicrofeedDataQuery(ClientValue):
    def __init__(
        self,
        item_limit: Optional[int] = None,
        query: Optional[str] = None,
        view_fields: StringCollection = StringCollection(),
        view_fields_only: Optional[bool] = None,
    ):
        self.ItemLimit = item_limit
        self.Query = query
        self.ViewFields = view_fields
        self.ViewFieldsOnly = view_fields_only

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedDataQuery"
