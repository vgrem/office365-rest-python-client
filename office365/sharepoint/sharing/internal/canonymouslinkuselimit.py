from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class CAnonymousLinkUseLimit(ClientValue):
    dailyLimitPerSite: int | None = None
    expiration: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Sharing.Internal.CAnonymousLinkUseLimit"
