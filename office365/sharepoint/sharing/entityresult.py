from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.entityresultdescription import (
    SharingEntityResultDescription,
)


@dataclass
class SharingEntityResult(ClientValue):
    Description: SharingEntityResultDescription = field(default_factory=SharingEntityResultDescription)
    Key: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingEntityResult"
