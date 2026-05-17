from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class SPContentEventsCustomEmailProperty(ClientValue):
    def __init__(
        self,
        category: Optional[int] = None,
        email_addresses: StringCollection = StringCollection(),
    ):
        self.Category = category
        self.EmailAddresses = email_addresses

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.SPContentEventsCustomEmailProperty"
