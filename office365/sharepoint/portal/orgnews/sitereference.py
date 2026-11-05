from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class PortalAndOrgNewsSiteReference(ClientValue):
    IsInDraftMode: bool | None = None
    IsVivaBackend: bool | None = None
    IsVivaHomeOptedOut: bool | None = None
    SiteId: UUID | None = None
    WebId: UUID | None = None
