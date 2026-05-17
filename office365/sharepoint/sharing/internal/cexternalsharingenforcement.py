from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class CExternalSharingEnforcement(ClientValue):
    def __init__(self, enforce_block: Optional[bool] = None, expiration: Optional[datetime] = None):
        self.enforceBlock = enforce_block
        self.expiration = expiration

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Sharing.Internal.CExternalSharingEnforcement"
