from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ChannelSummary(ClientValue):
    guestsCount: int | None = None
    hasMembersFromOtherTenants: bool | None = None
    membersCount: int | None = None
    ownersCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChannelSummary"
