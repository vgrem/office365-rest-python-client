from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPOContentSecurityPolicyEntry(ClientValue):

    def __init__(
        self, manual: bool = None, modified: datetime = None, source: str = None
    ):
        self.Manual = manual
        self.Modified = modified
        self.Source = source

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOContentSecurityPolicyEntry"
