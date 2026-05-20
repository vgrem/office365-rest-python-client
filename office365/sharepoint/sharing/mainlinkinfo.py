from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.principal import Principal


@dataclass
class MainLinkInfo(ClientValue):
    accessors: ClientValueCollection[Principal] = field(default_factory=lambda: ClientValueCollection(Principal))
    audience: int | None = None
    role: int | None = None
    shareId: UUID | None = None
    url: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkInfo"
