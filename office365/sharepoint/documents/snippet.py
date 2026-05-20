from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


@dataclass
class Snippet(ClientValue):
    Id: Optional[str] = None
    Name: Optional[str] = None
    Placeholders: ClientValueCollection[PlaceholderV2] = field(
        default_factory=lambda: ClientValueCollection(PlaceholderV2)
    )
    SnippetLibraryMappedId: Optional[str] = None
    SnippetLibraryMappedVersion: Optional[str] = None
