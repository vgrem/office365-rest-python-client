from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.teams.sp_team_channel_capabilities import SPTeamChannelCapabilities


class ManageChannelCapabilitiesRequest(ClientValue):
    SiteId: UUID | None = None
    TeamsChannelType: int | None = None
    ChannelCapabilities: SPTeamChannelCapabilities = field(default_factory=SPTeamChannelCapabilities)
