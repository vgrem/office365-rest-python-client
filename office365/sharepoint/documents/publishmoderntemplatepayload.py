from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.location import DocumentLocation
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2
from office365.sharepoint.documents.snippet import Snippet


@dataclass
class PublishModernTemplatePayload(ClientValue):
    DisableSearchAndApprovals: Optional[bool] = None
    Placeholders: ClientValueCollection[PlaceholderV2] = field(
        default_factory=lambda: ClientValueCollection(PlaceholderV2)
    )
    Snippets: ClientValueCollection[Snippet] = field(default_factory=lambda: ClientValueCollection(Snippet))
    Url: Optional[str] = None
    DocumentLocation: DocumentLocation = field(default_factory=DocumentLocation)
