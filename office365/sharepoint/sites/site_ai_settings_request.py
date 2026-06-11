from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class SiteAISettingsRequest(ClientValue):
    SiteId: UUID | None = None
    SiteUrl: str | None = None
