from office365.runtime.client_value import ClientValue


class LogActivityRequest(ClientValue):
    def __init__(self, last_access_time: str = None, list_item_unique_id: str = None):
        self.LastAccessTime = last_access_time
        self.ListItemUniqueId = list_item_unique_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.LogActivityRequest"
