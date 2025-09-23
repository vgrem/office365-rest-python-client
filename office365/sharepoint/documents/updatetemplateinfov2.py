from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.documents.contentassemblymoderntemplatecolumnsmappinginfo import (
    PlaceholderV2,
)


class UpdateTemplateInfoV2(ClientValue):

    def __init__(
        self,
        deleted_placeholder_column_ids: StringCollection = StringCollection(),
        new_name: str = None,
        operation: int = None,
        placeholders: ClientValueCollection[PlaceholderV2] = ClientValueCollection(
            PlaceholderV2
        ),
        set_template_view_as_default_view: bool = None,
        url: str = None,
    ):
        self.deleted_placeholder_column_ids = deleted_placeholder_column_ids
        self.new_name = new_name
        self.operation = operation
        self.placeholders = placeholders
        self.set_template_view_as_default_view = set_template_view_as_default_view
        self.url = url
