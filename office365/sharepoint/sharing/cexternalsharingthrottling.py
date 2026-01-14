from datetime import datetime

from office365.runtime.client_value import ClientValue


class CExternalSharingThrottling(ClientValue):
    def __init__(self, expiration: datetime = None, limit_level: int = None):
        self.expiration = expiration
        self.limitLevel = limit_level

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Sharing.Internal.CExternalSharingThrottling"
