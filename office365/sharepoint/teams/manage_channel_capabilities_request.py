from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class ManageChannelCapabilitiesRequest(ClientValue):
    SiteId: UUID | None = None
    TeamsChannelType: int | None = None
