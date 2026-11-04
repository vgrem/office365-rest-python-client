from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.sites.manager.content_part import ContentPart


@value
class MessageEntry(ClientValue):
    """content: str"""

    Role: Optional[str] = None
    Content: str | None = None
    ContentParts: ClientValueCollection[ContentPart] = field(default_factory=lambda: ClientValueCollection(ContentPart))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.MessageEntry"
