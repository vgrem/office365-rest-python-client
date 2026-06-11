from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2
from office365.sharepoint.documents.snippet import Snippet


@dataclass
class PublishTemplateV2Payload(ClientValue):
    DestinationListContentTypeId: str | None = None
    DestinationSiteContentTypeId: str | None = None
    Placeholders: ClientValueCollection[PlaceholderV2] = field(
        default_factory=lambda: ClientValueCollection(PlaceholderV2)
    )
    Snippets: ClientValueCollection[Snippet] = field(default_factory=lambda: ClientValueCollection(Snippet))
    Url: str | None = None
