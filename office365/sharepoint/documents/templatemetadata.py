from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholder import Placeholder


@dataclass
class TemplateMetaData(ClientValue):
    placeholders: ClientValueCollection[Placeholder] = field(default_factory=lambda: ClientValueCollection(Placeholder))
    server_redirected_embed_url: Optional[str] = None
