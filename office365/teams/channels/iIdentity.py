from typing import Optional

from office365.runtime.client_value import ClientValue


class ChannelIdentity(ClientValue):
    """Contains basic identification information about a channel in Microsoft Teams."""

    def __init__(self, channel_id: Optional[str] = None, team_id: Optional[str] = None) -> None:
        self.channelId = channel_id
        self.teamId = team_id
