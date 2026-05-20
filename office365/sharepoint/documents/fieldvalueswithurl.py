from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.cafieldvalue import CAFieldValue


@dataclass
class FieldValuesWithUrl(ClientValue):
    field_values: ClientValueCollection[CAFieldValue] = field(
        default_factory=lambda: ClientValueCollection(CAFieldValue)
    )
    server_redirected_embed_url: Optional[str] = None
