from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


@dataclass
class UpdateTemplateInfoV2(ClientValue):
    DeletedPlaceholderColumnIds: StringCollection = field(default_factory=StringCollection)
    NewName: str | None = None
    Operation: int | None = None
    Placeholders: ClientValueCollection[PlaceholderV2] = field(
        default_factory=lambda: ClientValueCollection(PlaceholderV2)
    )
    SetTemplateViewAsDefaultView: bool | None = None
    Url: str | None = None
