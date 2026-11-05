from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholder import Placeholder


class UpdateTemplateInfo(ClientValue):
    NewName: str | None = None
    Operation: int | None = None
    Placeholders: ClientValueCollection[Placeholder] = field(default_factory=lambda: ClientValueCollection(Placeholder))
