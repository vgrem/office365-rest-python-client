from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.columntypeinfo import ColumnTypeInfo
from office365.sharepoint.documents.contentassemblyfileinfo import (
    ContentAssemblyFileInfo,
)
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


class TemplatizationMetaData(ClientValue):

    def __init__(
        self,
        file_info: ContentAssemblyFileInfo = ContentAssemblyFileInfo(),
        is_template_view_default: bool = None,
        placeholder_column_type_info: ClientValueCollection[
            ColumnTypeInfo
        ] = ClientValueCollection(ColumnTypeInfo),
        placeholders: ClientValueCollection[PlaceholderV2] = ClientValueCollection(
            PlaceholderV2
        ),
    ):
        self.FileInfo = file_info
        self.IsTemplateViewDefault = is_template_view_default
        self.PlaceholderColumnTypeInfo = placeholder_column_type_info
        self.Placeholders = placeholders
