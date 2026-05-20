from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholder import Placeholder


@dataclass
class UpdateTemplateInfo(ClientValue):
    new_name: Optional[str] = None
    operation: Optional[int] = None
    placeholders: ClientValueCollection[Placeholder] = field(default_factory=lambda: ClientValueCollection(Placeholder))
