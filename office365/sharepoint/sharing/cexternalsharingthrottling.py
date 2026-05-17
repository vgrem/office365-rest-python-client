from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class CExternalSharingThrottling(ClientValue):
    def __init__(self, expiration: Optional[datetime] = None, limit_level: Optional[int] = None):
        self.expiration = expiration
        self.limitLevel = limit_level

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Sharing.Internal.CExternalSharingThrottling"
