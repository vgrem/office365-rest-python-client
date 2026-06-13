from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.content_part import ContentPart


@dataclass
class MessageEntry(ClientValue):
    """content: str"""

    Role: Optional[str] = None
    Content: str | None = None
    ContentParts: ClientValueCollection[ContentPart] = field(default_factory=lambda: ClientValueCollection(ContentPart))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.MessageEntry"
