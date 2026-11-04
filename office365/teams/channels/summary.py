from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ChannelSummary(ClientValue):
    guestsCount: int | None = None
    hasMembersFromOtherTenants: bool | None = None
    membersCount: int | None = None
    ownersCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChannelSummary"
