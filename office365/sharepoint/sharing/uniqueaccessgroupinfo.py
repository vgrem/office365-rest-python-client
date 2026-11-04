from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UniqueAccessGroupInfo(ClientValue):
    enabled: bool | None = None
    groupId: UUID | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.UniqueAccessGroupInfo"
