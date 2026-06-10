from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.audience import Audience


@dataclass
class TargetedSiteDetails(ClientValue):
    Audiences: ClientValueCollection[Audience] = field(default_factory=lambda: ClientValueCollection(Audience))
    IsInDraftMode: bool | None = None
    IsVivaBackendSite: bool | None = None
    SiteId: UUID | None = None
    TargetedLicenseType: int | None = None
    Title: str | None = None
    Url: str | None = None
    VivaConnectionsDefaultStart: bool | None = None
    WebId: UUID | None = None
