from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class KnowledgeHubSiteReference(ClientValue):
    SiteId: UUID | None = None
    Url: str | None = None
    WebId: UUID | None = None
