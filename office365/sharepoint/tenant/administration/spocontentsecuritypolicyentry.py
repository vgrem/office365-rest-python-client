from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPOContentSecurityPolicyEntry(ClientValue):
    def __init__(self, manual: Optional[bool] = None, modified: Optional[datetime] = None, source: Optional[str] = None):
        self.Manual = manual
        self.Modified = modified
        self.Source = source

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOContentSecurityPolicyEntry"
