from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class CExternalSharingThrottling(ClientValue):
    expiration: datetime | None = None
    limitLevel: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Sharing.Internal.CExternalSharingThrottling"
