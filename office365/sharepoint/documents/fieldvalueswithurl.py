from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.documents.cafieldvalue import CAFieldValue


@value
class FieldValuesWithUrl(ClientValue):
    FieldValues: ClientValueCollection[CAFieldValue] = field(default_factory=lambda: ClientValueCollection(CAFieldValue))
    ServerRedirectedEmbedUrl: str | None = None
