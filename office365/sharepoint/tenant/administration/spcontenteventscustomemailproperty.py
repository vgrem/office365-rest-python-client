from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SPContentEventsCustomEmailProperty(ClientValue):
    def __init__(
        self,
        category: int = None,
        email_addresses: StringCollection = StringCollection(),
    ):
        self.Category = category
        self.EmailAddresses = email_addresses

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.SPContentEventsCustomEmailProperty"
