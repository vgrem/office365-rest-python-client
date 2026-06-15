from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class AuthoritativeResourceProperties(ClientValue):
    IsAuthoritativeSetBy: str | None = None
    IsAuthoritativeSetByUpn: str | None = None
    IsAuthoritativeSetByUserId: str | None = None
    IsAuthoritativeSetDate: datetime | None = field(default_factory=lambda: datetime.min)
    SiteId: UUID | None = None
    SiteTitle: str | None = None
    SiteUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.AuthoritativeResourceProperties"
