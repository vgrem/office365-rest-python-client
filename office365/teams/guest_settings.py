from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamGuestSettings(ClientValue):
    """Settings to configure whether guests can create, update, or delete channels in the team.

    Args:
        allow_create_update_channels (bool):
        allow_delete_channels (bool):
    """

    allowCreateUpdateChannels: bool = True
    allowDeleteChannels: bool = True

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamGuestSettings"
