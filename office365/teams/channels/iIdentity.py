from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ChannelIdentity(ClientValue):
    """Contains basic identification information about a channel in Microsoft Teams."""

    channelId: str | None = None
    teamId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChannelIdentity"
