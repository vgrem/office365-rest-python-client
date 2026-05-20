from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class CExternalSharingThrottling(ClientValue):
    expiration: datetime | None = None
    limitLevel: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Sharing.Internal.CExternalSharingThrottling"
