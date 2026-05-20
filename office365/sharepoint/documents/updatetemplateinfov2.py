from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


@dataclass
class UpdateTemplateInfoV2(ClientValue):
    deleted_placeholder_column_ids: StringCollection = field(default_factory=StringCollection)
    new_name: Optional[str] = None
    operation: Optional[int] = None
    placeholders: ClientValueCollection[PlaceholderV2] = field(
        default_factory=lambda: ClientValueCollection(PlaceholderV2)
    )
    set_template_view_as_default_view: Optional[bool] = None
    url: Optional[str] = None
