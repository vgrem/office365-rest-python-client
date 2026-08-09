from __future__ import annotations

from dataclasses import dataclass

from office365.communications.onlinemeetings.lobbybypassscope import LobbyBypassScope
from office365.runtime.client_value import ClientValue


@dataclass
class LobbyBypassSettings(ClientValue):
    isDialInBypassEnabled: bool | None = None
    scope: LobbyBypassScope = LobbyBypassScope.organizer

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LobbyBypassSettings"
