from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection
from office365.runtime.types.value import value


@value
class HomeSiteReference(ClientValue):
    Audiences: GuidCollection = field(default_factory=GuidCollection)
    SiteFlags: int | None = None
    SiteId: UUID | None = None
    WebId: UUID | None = None
