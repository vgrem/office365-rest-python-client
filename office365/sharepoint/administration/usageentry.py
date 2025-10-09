from office365.runtime.client_value import ClientValue


class UsageEntry(ClientValue):

    def __init__(
        self,
        event_type_id: int = None,
        item_id: str = None,
        scope_id: str = None,
        site: str = None,
        user: str = None,
    ):
        self.EventTypeId = event_type_id
        self.ItemId = item_id
        self.ScopeId = scope_id
        self.Site = site
        self.User = user

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.UsageEntry"
