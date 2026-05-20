from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.columntypeinfo import ColumnTypeInfo
from office365.sharepoint.documents.contentassemblyfileinfo import (
    ContentAssemblyFileInfo,
)
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


@dataclass
class TemplatizationMetaData(ClientValue):
    FileInfo: ContentAssemblyFileInfo = field(default_factory=ContentAssemblyFileInfo)
    IsTemplateViewDefault: Optional[bool] = None
    PlaceholderColumnTypeInfo: ClientValueCollection[ColumnTypeInfo] = field(
        default_factory=lambda: ClientValueCollection(ColumnTypeInfo)
    )
    Placeholders: ClientValueCollection[PlaceholderV2] = field(
        default_factory=lambda: ClientValueCollection(PlaceholderV2)
    )
