from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class HomeSiteReference(ClientValue):
    Audiences: GuidCollection = field(default_factory=GuidCollection)
    SiteFlags: int | None = None
    SiteId: UUID | None = None
    WebId: UUID | None = None
