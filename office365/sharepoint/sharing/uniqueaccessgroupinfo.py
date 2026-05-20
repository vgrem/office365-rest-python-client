from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class UniqueAccessGroupInfo(ClientValue):
    enabled: bool | None = None
    groupId: UUID | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.UniqueAccessGroupInfo"
