from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.cafieldvalue import CAFieldValue


@dataclass
class FieldValuesWithUrl(ClientValue):
    FieldValues: ClientValueCollection[CAFieldValue] = field(default_factory=lambda: ClientValueCollection(CAFieldValue))
    ServerRedirectedEmbedUrl: str | None = None
