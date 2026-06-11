from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ChannelCapabilities(ClientValue):
    HasOwningTeamAccess: bool | None = None
    IndirectB2BCollabMode: int | None = None
    IsB2BCollabEnabled: bool | None = None
    IsB2BDirectConnectEnabled: bool | None = None
    IsNextGenerationChannel: bool | None = None
    SiteMembershipIndicator: int | None = None
