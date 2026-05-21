from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class TenantCdnUrl(ClientValue):
    CdnUrl: str | None = None
    ExpirationTimeUtc: datetime | None = None
    IsCdnUrlAvailable: bool | None = None
    ItemUrl: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.TenantCdn.TenantCdnUrl"
