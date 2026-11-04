from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ChannelIdentity(ClientValue):
    """Contains basic identification information about a channel in Microsoft Teams."""

    channelId: str | None = None
    teamId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChannelIdentity"
