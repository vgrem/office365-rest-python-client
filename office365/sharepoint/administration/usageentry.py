from office365.runtime.client_value import ClientValue
from typing import Optional


class UsageEntry(ClientValue):
    def __init__(
        self,
        event_type_id: Optional[int] = None,
        item_id: Optional[str] = None,
        scope_id: Optional[str] = None,
        site: Optional[str] = None,
        user: Optional[str] = None,
    ):
        self.EventTypeId = event_type_id
        self.ItemId = item_id
        self.ScopeId = scope_id
        self.Site = site
        self.User = user

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.UsageEntry"
