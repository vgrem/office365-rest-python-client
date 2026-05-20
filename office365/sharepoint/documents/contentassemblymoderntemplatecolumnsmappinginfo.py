from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


@dataclass
class ContentAssemblyModernTemplateColumnsMappingInfo(ClientValue):
    destination_list_content_type_id: Optional[str] = None
    destination_site_content_type_id: Optional[str] = None
    placeholders: ClientValueCollection[PlaceholderV2] = field(
        default_factory=lambda: ClientValueCollection(PlaceholderV2)
    )
